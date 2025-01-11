import ee
#import geemap

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

# Sample image collection (e.g., 'LANDSAT/LC08/C02/T2_TOA')
s2 = ee.ImageCollection('LANDSAT/LC08/C02/T2_TOA') \
    .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']) \
    .filterDate(start_date, end_date) \
    .filterBounds(roi) \
    .map(lambda img: img.set('missDate', img.date().format('YYYY-MM-dd'))) \
    .sort('system:time_start')

# Function to select the brightest pixels
def select_brightest_pixels(image, roi, n=10):
    """
    Select the n brightest pixels from the image based on brightness.
    This function retains both geometry and band values of the brightest pixels.
    """
    # Compute brightness for each pixel by summing the selected bands
    brightness = image.select(['B2', 'B3', 'B4', 'B5', 'B6']).reduce(ee.Reducer.sum())

    # Sample the image to get pixel values within the region of interest (ROI)
    sampled_points = brightness.sample(region=roi, scale=30, numPixels=1000)

    # Sort the points by brightness in descending order
    sorted_points = sampled_points.sort('sum', False)  # Sort by 'sum' of brightness

    # Select the top n brightest points
    top_n_brightest_points = sorted_points.limit(n)

    return top_n_brightest_points

#Function to grab the average band values for endmembers
def get_average_of_brightest(image, roi, n=10):
    """
    For the top n brightest pixels, calculate the mean value for each band.
    This will return a list of mean values, one for each band.
    """
    # Select the brightest pixels
    brightest_points = select_brightest_pixels(image, roi, n)

    # Get the band names and apply the compute_mean function to each band
    bands = image.bandNames()

    # Initialize an empty list to store the mean values for each band
    def compute_mean(band):
        # Extract the values for the current band from the brightest points
        band_values = brightest_points.aggregate_array(band)

        # Check if the band has valid (non-null) values and compute mean
        def check_valid(band_values):
            return band_values.size().gt(0)  # Check if list has values

        valid_values = check_valid(band_values)

        # If there are valid values, compute the mean; otherwise, return 0
        mean_value = ee.Algorithms.If(
            valid_values,
            band_values.reduce(ee.Reducer.mean()),
            ee.Number(0)  # Default to 0 if no valid values
        )

        return mean_value

    # Apply compute_mean to each band and return the list of means
    mean_values_list = bands.map(compute_mean)

    return mean_values_list


# Function to define endmembers
def define_endmembers(image, roi, roi_soil, n=10):
    # Calculate mean values for each band of the brightest pixels ("ice" endmember)
    brightest_pixel_means = get_average_of_brightest(image, roi, n)

    # If no valid means are found, return None
    if ee.List(brightest_pixel_means).size().getInfo() == 0:
        print("Error: No valid brightest pixel means calculated.")
        return None

    # Calculate mean values for each band within the soil ROI ("soil" endmember)
    soil_mean = soil_mean_defined  # Already defined elsewhere

    # Define endmembers as a list of lists
    endmembers = [brightest_pixel_means, soil_mean] 

    return endmembers

# Function to perform spectral unmixing
def perform_unmixing(image, endmembers):
    if endmembers is None:
        return None

    # Extract endmembers from the list
    brightest_pixel_means = ee.List(endmembers[0])
    soil_mean = ee.List(endmembers[1])

    # Perform unmixing
    unmixed_image = image.unmix([brightest_pixel_means, soil_mean])

    return unmixed_image.set('system:time_start', image.get('system:time_start'))

# Apply the process_images function to the image collection
def process_images(image):
    # Define endmembers for the current image
    endmembers = define_endmembers(image, roi, roi_soil)
    
    # If endmembers are None, skip the unmixing process
    if endmembers is None:
        return None
    
    # Perform unmixing on the current image
    unmixed_image = perform_unmixing(image, endmembers)

    return unmixed_image

# Process each image in the collection (server-side processing)
processed_images = s2.map(process_images)

# Check results
print(processed_images.size().getInfo())
