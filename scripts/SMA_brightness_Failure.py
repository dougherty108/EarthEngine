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

ids = ee.List(['LANDSAT_8_2016-11-02', 'LANDSAT_8_2016-11-04', 'LANDSAT_8_2016-11-06', 'LANDSAT_8_2016-11-08', 'LANDSAT_8_2016-11-13', 'LANDSAT_8_2016-11-15', 'LANDSAT_8_2016-12-10', 'LANDSAT_8_2016-12-13', 'LANDSAT_8_2016-12-15', 'LANDSAT_8_2016-12-17', 'LANDSAT_8_2016-12-19', 'LANDSAT_8_2016-12-24', 'LANDSAT_8_2017-01-02', 'LANDSAT_8_2017-01-11', 'LANDSAT_8_2017-01-14', 'LANDSAT_8_2017-01-18', 'LANDSAT_8_2017-01-25', 'LANDSAT_8_2017-01-27', 'LANDSAT_8_2017-01-30', 'LANDSAT_8_2017-02-01', 'LANDSAT_8_2017-11-04', 'LANDSAT_8_2017-11-07', 'LANDSAT_8_2017-11-18', 'LANDSAT_8_2017-11-20', 'LANDSAT_8_2017-11-21', 'LANDSAT_8_2017-11-25', 'LANDSAT_8_2017-11-27', 'LANDSAT_8_2017-11-30', 'LANDSAT_8_2017-12-02', 'LANDSAT_8_2017-12-07', 'LANDSAT_8_2017-12-16', 'LANDSAT_8_2017-12-23', 'LANDSAT_8_2018-01-03', 'LANDSAT_8_2018-01-05', 'LANDSAT_8_2018-01-07', 'LANDSAT_8_2018-01-10', 'LANDSAT_8_2018-01-12', 'LANDSAT_8_2018-01-14', 'LANDSAT_8_2018-01-19', 'LANDSAT_8_2018-01-26', 'LANDSAT_8_2018-01-30', 'LANDSAT_8_2018-11-05', 'LANDSAT_8_2018-11-07', 'LANDSAT_8_2018-11-08', 'LANDSAT_8_2018-11-12', 'LANDSAT_8_2018-11-17', 'LANDSAT_8_2018-11-19', 'LANDSAT_8_2018-11-23', 'LANDSAT_8_2018-11-24', 'LANDSAT_8_2018-11-26', 'LANDSAT_8_2018-11-28', 'LANDSAT_8_2018-11-30', 'LANDSAT_8_2018-12-05', 'LANDSAT_8_2018-12-30', 'LANDSAT_8_2019-01-01', 'LANDSAT_8_2019-01-04', 'LANDSAT_8_2019-01-06', 'LANDSAT_8_2019-01-10', 'LANDSAT_8_2019-01-11', 'LANDSAT_8_2019-01-15', 'LANDSAT_8_2019-01-24', 'LANDSAT_8_2019-01-26', 'LANDSAT_8_2019-11-06', 'LANDSAT_8_2019-11-08', 'LANDSAT_8_2019-11-10', 'LANDSAT_8_2019-11-11', 'LANDSAT_8_2019-11-15', 'LANDSAT_8_2019-11-17', 'LANDSAT_8_2019-11-24', 'LANDSAT_8_2019-11-26', 'LANDSAT_8_2019-11-27', 'LANDSAT_8_2019-12-03', 'LANDSAT_8_2019-12-17', 'LANDSAT_8_2019-12-24', 'LANDSAT_8_2019-12-26', 'LANDSAT_8_2019-12-31', 'LANDSAT_8_2020-01-02', 'LANDSAT_8_2020-01-11', 'LANDSAT_8_2020-01-20', 'LANDSAT_8_2020-10-30', 'LANDSAT_8_2020-11-15', 'LANDSAT_8_2020-11-17', 'LANDSAT_8_2020-11-19', 'LANDSAT_8_2020-11-24', 'LANDSAT_8_2020-11-26', 'LANDSAT_8_2020-11-28', 'LANDSAT_8_2020-11-29', 'LANDSAT_8_2020-12-01', 'LANDSAT_8_2020-12-03', 'LANDSAT_8_2020-12-08', 'LANDSAT_8_2020-12-10', 'LANDSAT_8_2020-12-14', 'LANDSAT_8_2020-12-15', 'LANDSAT_8_2020-12-21', 'LANDSAT_8_2020-12-24', 'LANDSAT_8_2020-12-26', 'LANDSAT_8_2020-12-30', 'LANDSAT_8_2021-01-06', 'LANDSAT_8_2021-01-13', 'LANDSAT_8_2021-01-15', 'LANDSAT_8_2021-01-16', 'LANDSAT_8_2021-01-18', 'LANDSAT_8_2021-01-22', 'LANDSAT_8_2021-02-01', 'LANDSAT_8_2021-10-31', 'LANDSAT_8_2021-11-04', 'LANDSAT_8_2021-11-09', 'LANDSAT_8_2021-11-11', 'LANDSAT_8_2021-11-15', 'LANDSAT_8_2021-11-20', 'LANDSAT_8_2021-12-01', 'LANDSAT_8_2021-12-02', 'LANDSAT_8_2021-12-04', 'LANDSAT_8_2021-12-06', 'LANDSAT_8_2021-12-08', 'LANDSAT_8_2021-12-11', 'LANDSAT_8_2021-12-18', 'LANDSAT_8_2021-12-20', 'LANDSAT_8_2021-12-22', 'LANDSAT_8_2021-12-24', 'LANDSAT_8_2022-01-05', 'LANDSAT_8_2022-01-07', 'LANDSAT_8_2022-01-12', 'LANDSAT_8_2022-01-14', 'LANDSAT_8_2022-01-16', 'LANDSAT_8_2022-01-19', 'LANDSAT_8_2022-01-25', 'LANDSAT_8_2022-01-28', 'LANDSAT_8_2022-11-14', 'LANDSAT_8_2022-11-16', 'LANDSAT_8_2022-11-18', 'LANDSAT_8_2022-11-19', 'LANDSAT_8_2022-11-21', 'LANDSAT_8_2022-11-23', 'LANDSAT_8_2022-11-28', 'LANDSAT_8_2022-12-04', 'LANDSAT_8_2022-12-05', 'LANDSAT_8_2022-12-11', 'LANDSAT_8_2022-12-16', 'LANDSAT_8_2022-12-18', 'LANDSAT_8_2023-01-01', 'LANDSAT_8_2023-01-03', 'LANDSAT_8_2023-01-10', 'LANDSAT_8_2023-01-15', 'LANDSAT_8_2023-01-22', 'LANDSAT_8_2023-01-24', 'LANDSAT_8_2023-11-01', 'LANDSAT_8_2023-11-17', 'LANDSAT_8_2023-11-19', 'LANDSAT_8_2023-11-21', 'LANDSAT_8_2023-12-05', 'LANDSAT_8_2023-12-07', 'LANDSAT_8_2023-12-10', 'LANDSAT_8_2023-12-19', 'LANDSAT_8_2023-12-28', 'LANDSAT_8_2023-12-30', 'LANDSAT_8_2024-01-04', 'LANDSAT_8_2024-01-11', 'LANDSAT_8_2024-01-13', 'LANDSAT_8_2024-01-22', 'LANDSAT_8_2024-01-24'])

def addImageDate(image):
    mission = image.get('SPACECRAFT_ID')
    date = image.date().format('YYYY-MM-dd')
    missDate = ee.String(mission).cat('_').cat(ee.String(date))
    return image.set('missDate', missDate)

def mosaic_by_date(imcol):
    # Convert the image collection to a list of images
    imlist = imcol.toList(imcol.size())
    
    # Get unique dates from the image collection
    def get_date(image):
        return ee.Image(image).date().format("YYYY-MM-dd")
    
    unique_dates = imlist.map(lambda im: get_date(im)).distinct()

    def create_mosaic(date_str):
        date = ee.Date(date_str)
        
        # Filter images for that day and create a mosaic
        mosaic = imcol.filterDate(date, date.advance(1, 'day')).mosaic()
        
        return mosaic.set({
            'system:time_start': date.millis(),
            'system:id': date.format('YYYY-MM-dd')
        })

    # Create mosaics for each unique date
    mosaic_imlist = unique_dates.map(create_mosaic)
    
    return ee.ImageCollection(mosaic_imlist)

# Example usage with an image collection (e.g., 'LANDSAT/LC08/C02/T1_L2')
s2 = ee.ImageCollection('LANDSAT/LC08/C02/T2_TOA')\
    .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'])\
    .filterDate(start_date, end_date)\
    .map(addImageDate)\
    .filter(ee.Filter.inList("missDate", ids))\
    .filter(ee.Filter.gt('SUN_ELEVATION',20))\
    .filterBounds(roi)\
    .sort('DATE_ACQUIRED')
s3 = mosaic_by_date(s2)

# Clip all the images in the s3 collection down to the ROI
def clip_image(image):
    return image.clip(roi)

# Apply clip to image collection
l8_clipped = s3.map(clip_image)

print(l8_clipped.size().getInfo())

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