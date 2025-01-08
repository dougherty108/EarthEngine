import ee
import numpy

# Authenticates the session with EE
ee.Authenticate()

# Creates the connection with EE.
ee.Initialize()

# Define ROI for soil
roi_soil = ee.Geometry.Rectangle([163.078070, -77.625204, 163.07800, -77.625340])

# Define ROI for analysis
roi = ee.Geometry.Rectangle([162.277817, -77.740157, 163.272100, -77.576571])

# Define start and end date for the image collection filter
start_date = "2016-03-06"
end_date = "2025-01-01"

# Select Landsat 8 Collection
s2 = ee.ImageCollection('LANDSAT/LC08/C02/T2_TOA') \
    .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']) \
    .filterDate(start_date, end_date) \
    .filterBounds(roi) \
    .sort('DATE_ACQUIRED')

# Create a mosaic by date
def mosaic_by_date(imcol):
    """
    Create a mosaic for each unique date in the image collection.
    """
    imlist = imcol.toList(imcol.size())

    def get_date(image):
        return ee.Image(image).date().format("YYYY-MM-dd")

    unique_dates = imlist.map(lambda im: get_date(im)).distinct()

    def create_mosaic(date_str):
        date = ee.Date(date_str)
        mosaic = imcol.filterDate(date, date.advance(1, 'day')).mosaic()
        return mosaic.set({
            'system:time_start': date.millis(),
            'system:id': date.format('YYYY-MM-dd')
        })

    mosaic_imlist = unique_dates.map(create_mosaic)
    return ee.ImageCollection(mosaic_imlist)

s3 = mosaic_by_date(s2)

# Clip all the images in the s3 collection down to the ROI
def clip_image(image):
    return image.clip(roi)

# Apply clip to image collection
l8_clipped = s3.map(clip_image)

## Define the Soil Endmember
# define soil endmember from a single image
#define ROI
roi_soil = ee.Geometry.Rectangle([163.078070, -77.625204, 163.07800, -77.625340])

#pull image
soil1 = ee.Image('LANDSAT/LC08/C02/T2_TOA/LC08_055116_20231205').select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'])

#clip image down to ROI for soil
soil = soil1.clip(roi_soil)

#reduce down to mean for endmembers. 
soil_mean_defined = soil.reduceRegion(ee.Reducer.mean()).values()

# Function to select brightest pixels
def select_brightest_pixels(image, roi, n=10):
    """
    Select the n brightest pixels from the image based on brightness.
    """
    # Compute brightness for each pixel by summing the selected bands (e.g., B2, B3, B4, etc.)
    brightness = image.select(['B6']).reduce(ee.Reducer.sum())

    # Sample the image to get pixel values within the region of interest (ROI)
    sampled_points = brightness.sample(region=roi, scale=30, numPixels=1000)

    # Sort the points by brightness in descending order
    sorted_points = sampled_points.sort('sum', False)  # Sort by 'sum' of brightness

    # Select the top n brightest points
    top_n_brightest_points = sorted_points.limit(n)
    return top_n_brightest_points

# Function to get average of brightest pixels (Server-side operation only)
def get_average_of_brightest(image, roi, n=10):
    # Select the brightest pixels
    brightest_points = select_brightest_pixels(image, roi, n)

    # Get the band names
    bands = image.bandNames()

    mean_values_list = []

    # For each band, compute the mean value from the brightest points
    for band in bands.getInfo():  # Use .getInfo() to iterate over band names
        # Extract the values for the current band from the brightest points
        band_values = brightest_points.aggregate_array(band)

        # Compute the mean of the extracted band values
        mean_value = band_values.reduce(ee.Reducer.mean())

        # Append the mean value to the list
        mean_values_list.append(mean_value)

    return ee.List(mean_values_list)

# Function to define endmembers (Server-side operations only)
def define_endmembers(image, roi, roi_soil, n=10):

    # Calculate mean values for each band of the brightest pixels ("ice" endmember)
    brightest_pixel_means = get_average_of_brightest(image, roi, n) 

    # Calculate mean values for each band within the soil ROI ("soil" endmember)
    soil_mean = soil_mean_defined

    # Define endmembers as a list of lists
    endmembers = [brightest_pixel_means, soil_mean] 

    return endmembers


# Function to perform spectral unmixing
def perform_unmixing(image, endmembers):
    # Extract endmembers from the list
    brightest_pixel_means = endmembers[0]
    soil_mean = endmembers[1]

    # Define endmembers for the unmix function (server-side)
    unmix_endmembers = [ee.List(brightest_pixel_means), ee.List(soil_mean)]

    unmixed_image = image.unmix(unmix_endmembers, True, True)

    return unmixed_image.set('system:time_start', image.get('system:time_start'))


# Process each image in the collection (Server-side processing)
def process_images(image):
    endmembers = define_endmembers(image, roi, roi_soil) 
    unmixed_image = perform_unmixing(image, endmembers) 
    return unmixed_image

# Apply the process_images function to the filtered image collection l8_clipped (Server-side processing)
processed_images = l8_clipped.map(process_images)

# Print processed image information (Server-side access, no client-side .getInfo())
# Instead of getInfo(), you can use ee.ImageCollection.getInfo() or other server-side methods as necessary
first_image = processed_images.first()
print(first_image.get('system:id').getInfo())  # Example of using server-side information


############ TROUBLE SHOOTING ###########
##### load a random image to test all of the functions on individually for trouble shooting

# Pull the image for the soil endmember
soil1 = ee.Image('LANDSAT/LC08/C02/T2_TOA/LC08_055116_20231205').select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'])

#Function 0
# Compute brightness for each pixel by summing the selected bands (e.g., B2, B3, B4, etc.)
brightness = soil1.select(['B2', 'B3', 'B4', 'B5', 'B6']).reduce(ee.Reducer.sum())
print(brightness.getInfo())
# Sample the image to get pixel values within the region of interest (ROI)
sampled_points = brightness.sample(region=roi, scale=30, numPixels=1000)
print(sampled_points.getInfo())
# Sort the points by brightness in descending order
sorted_points = sampled_points.sort('sum', False)  # Sort by 'sum' of brightness
print(sorted_points.getInfo())
# Select the top n brightest points
top_n_brightest_points = sorted_points.limit(10)
print(top_n_brightest_points.getInfo())

#Function 1
# Select the brightest pixels
brightest_points = select_brightest_pixels(soil1, roi, 10)

    # Get a list of band names
bands = soil1.bandNames()

    # Calculate the mean value for each band using the brightest pixels
    #mean_values = brightest_points.reduceColumns(
    #    reducer=ee.Reducer.mean(),
    #    selectors=bands
    #)
    
    # Loop through each band and calculate the mean for each one separately
mean_values = []
for band in bands.getInfo():
        # For each band, reduce the values of the brightest pixels to get the mean
    mean_band = brightest_points.aggregate_stats(band).get('mean')
    mean_values.append(mean_band)

    # Extract the mean values as a list from the result (this is now a List of averages)
mean_values_list = ee.List(mean_values)
print(mean_values_list.getInfo())


#Function 2
# Calculate mean values for each band of the brightest pixels ("ice" endmember)
brightest_pixel_means = get_average_of_brightest(soil1, roi) 

# Calculate mean values for each band within the soil ROI ("soil" endmember)
soil_mean = soil1.reduceRegion(ee.Reducer.mean(), roi_soil, 30).values()

# Define endmembers as a list of lists
endmembers = [brightest_pixel_means, soil_mean] 

#Function 3
# Extract endmembers from the list
brightest_pixel_means = endmembers[0]
soil_mean = endmembers[1]
print(brightest_pixel_means.getInfo())

# Define endmembers for the unmix function (server-side)
unmix_endmembers = [brightest_pixel_means, soil_mean]

unmixed_image = soil1.unmix(unmix_endmembers, True, True)
print(unmixed_image.getInfo())

#if you run everything individually, it works. In function form in the above portion of the script, it does not. 


## script try again
import ee
import numpy as np

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize()

# Define ROIs
roi_soil = ee.Geometry.Rectangle([163.078070, -77.625204, 163.07800, -77.625340])
roi = ee.Geometry.Rectangle([162.277817, -77.740157, 163.272100, -77.576571])

# Define date range
start_date = "2016-03-06"
end_date = "2025-01-01"

# Select Landsat 8 Collection
s2 = ee.ImageCollection('LANDSAT/LC08/C02/T2_TOA') \
    .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']) \
    .filterDate(start_date, end_date) \
    .filterBounds(roi) \
    .sort('DATE_ACQUIRED')

def mosaic_by_date(imcol):
    """Create a mosaic for each unique date in the image collection."""
    def get_date(image):
        return ee.Image(image).date().format("YYYY-MM-dd")

    def create_mosaic(date_str):
        date = ee.Date(date_str)
        mosaic = imcol.filterDate(date, date.advance(1, 'day')).mosaic()
        return mosaic.set({
            'system:time_start': date.millis(),
            'system:id': date.format('YYYY-MM-dd')
        })

    unique_dates = imcol.map(get_date).distinct()
    return ee.ImageCollection(unique_dates.map(create_mosaic))

s3 = mosaic_by_date(s2)

# Clip all images in the s3 collection to the ROI
l8_clipped = s3.map(lambda image: image.clip(roi))

# Define soil endmember
soil1 = ee.Image('LANDSAT/LC08/C02/T2_TOA/LC08_055116_20231205').select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'])
soil = soil1.clip(roi_soil)
soil_mean_defined = soil.reduceRegion(ee.Reducer.mean()).values()

def select_brightest_pixels(image, roi, n=10):
    """Select the n brightest pixels from the image based on brightness."""
    brightness = image.select(['B6']).reduce(ee.Reducer.sum())
    sampled_points = brightness.sample(region=roi, scale=30, numPixels=1000)
    sorted_points = sampled_points.sort('sum', False)
    return sorted_points.limit(n)

def get_average_of_brightest(image, roi, n=10):
    brightest_points = select_brightest_pixels(image, roi, n)
    bands = image.bandNames()
    return ee.List(bands.map(lambda band: brightest_points.aggregate_mean(band)))

def define_endmembers(image, roi, roi_soil, n=10):
    brightest_pixel_means = get_average_of_brightest(image, roi, n)
    return [brightest_pixel_means, soil_mean_defined]

def perform_unmixing(image, endmembers):
    unmixed_image = image.unmix(endmembers, True, True)
    return unmixed_image.set('system:time_start', image.get('system:time_start'))

def process_images(image):
    endmembers = define_endmembers(image, roi, roi_soil)
    return perform_unmixing(image, endmembers)

# Apply the process_images function to the filtered image collection l8_clipped
processed_images = l8_clipped.map(process_images)

# Print processed image information
first_image = processed_images.first()
print(first_image.get('system:id').getInfo())
