##### Fryxell SMA workflow
# iniialize and load packages
import ee
import geemap

# Initialize Earth Engine
ee.Authenticate()
ee.Initialize()

# define ROIs
roi_LF = ee.Geometry.Polygon([[163.0750389287657,-77.61910477852867],
                               [163.11486436821883,-77.62293200514104],
                               [163.15056993462508,-77.62020890574621],
                               [163.15812303521102,-77.61682260842034],
                               [163.19245531060164,-77.61777969790991],
                               [163.21099473931258,-77.61063658212983],
                               [163.2223243901915,-77.60643718911331],
                               [163.25974657036727,-77.60761610752947],
                               [163.26832963921493,-77.60326829880877],
                               [163.2556266973204,-77.59759178135695],
                               [163.19829179741805,-77.60135183869454],
                               [163.18558885552352,-77.59670689887578],
                               [163.09529497124618,-77.60960528204666],
                               [163.09254838921493,-77.6127725777997],
                               [163.0643959233946,-77.61667535742002],
                               [163.0750389287657,-77.61910477852867]])

roi_LF_crop = ee.Geometry.Polygon([[163.10147025602208,-77.63763858931995],
                                   [163.31227042692052,-77.61056024754215],
                                   [163.23605277555333,-77.5841617068026],
                                   [163.02731254117833,-77.6108548909756],
                                   [163.10147025602208,-77.63763858931995]
])

pointed = ee.Geometry.BBox(162.1, -77.73, 163.3, -77.59)

ids = ee.List(["LANDSAT_8_2016-11-02", "LANDSAT_8_2016-11-04", "LANDSAT_8_2016-11-06", "LANDSAT_8_2016-11-08",
               "LANDSAT_8_2016-11-13", "LANDSAT_8_2016-11-15", "LANDSAT_8_2016-11-22", "LANDSAT_8_2016-11-24",
               "LANDSAT_8_2016-11-27", "LANDSAT_8_2016-12-08", "LANDSAT_8_2016-12-10", "LANDSAT_8_2016-12-13",
               "LANDSAT_8_2016-12-15", "LANDSAT_8_2016-12-17", "LANDSAT_8_2016-12-19", "LANDSAT_8_2016-12-24",
               "LANDSAT_8_2017-01-02", "LANDSAT_8_2017-01-09", "LANDSAT_8_2017-01-11", "LANDSAT_8_2017-01-14",
               "LANDSAT_8_2017-01-18", "LANDSAT_8_2017-01-25", "LANDSAT_8_2017-01-27", "LANDSAT_8_2017-01-30",
               "LANDSAT_8_2017-11-04", "LANDSAT_8_2017-11-07", "LANDSAT_8_2017-11-18", "LANDSAT_8_2017-11-20",
               "LANDSAT_8_2017-11-21", "LANDSAT_8_2017-11-25", "LANDSAT_8_2017-11-27", "LANDSAT_8_2017-11-30",
               "LANDSAT_8_2017-12-02", "LANDSAT_8_2017-12-07", "LANDSAT_8_2017-12-16", "LANDSAT_8_2017-12-23",
               "LANDSAT_8_2018-01-03", "LANDSAT_8_2018-01-05", "LANDSAT_8_2018-01-07", "LANDSAT_8_2018-01-10",
               "LANDSAT_8_2018-01-12", "LANDSAT_8_2018-01-14", "LANDSAT_8_2018-01-19", "LANDSAT_8_2018-01-26",
               "LANDSAT_8_2018-01-30", "LANDSAT_8_2018-11-05", "LANDSAT_8_2018-11-07", "LANDSAT_8_2018-11-08",
               "LANDSAT_8_2018-11-12", "LANDSAT_8_2018-11-17", "LANDSAT_8_2018-11-19", "LANDSAT_8_2018-11-24",
               "LANDSAT_8_2018-11-26", "LANDSAT_8_2018-11-28", "LANDSAT_8_2018-11-30", "LANDSAT_8_2018-12-05",
               "LANDSAT_8_2018-12-19", "LANDSAT_8_2018-12-25", "LANDSAT_8_2018-12-30", "LANDSAT_8_2019-01-01",
               "LANDSAT_8_2019-01-04", "LANDSAT_8_2019-01-06", "LANDSAT_8_2019-01-10", "LANDSAT_8_2019-01-11",
               "LANDSAT_8_2019-01-15", "LANDSAT_8_2019-01-24", "LANDSAT_8_2019-01-26", "LANDSAT_8_2019-01-27",
               "LANDSAT_8_2019-11-04", "LANDSAT_8_2019-11-06", "LANDSAT_8_2019-11-08", "LANDSAT_8_2019-11-10",
               "LANDSAT_8_2019-11-11", "LANDSAT_8_2019-11-15", "LANDSAT_8_2019-11-17", "LANDSAT_8_2019-11-24",
               "LANDSAT_8_2019-11-26", "LANDSAT_8_2019-11-27", "LANDSAT_8_2019-12-03", "LANDSAT_8_2019-12-10",
               "LANDSAT_8_2019-12-12", "LANDSAT_8_2019-12-17", "LANDSAT_8_2019-12-24", "LANDSAT_8_2019-12-26",
               "LANDSAT_8_2019-12-29", "LANDSAT_8_2019-12-31", "LANDSAT_8_2020-01-02", "LANDSAT_8_2020-01-11",
               "LANDSAT_8_2020-01-20", "LANDSAT_8_2020-10-30", "LANDSAT_8_2020-11-08", "LANDSAT_8_2020-11-15",
               "LANDSAT_8_2020-11-17", "LANDSAT_8_2020-11-19", "LANDSAT_8_2020-11-24", "LANDSAT_8_2020-11-26",
               "LANDSAT_8_2020-11-28", "LANDSAT_8_2020-11-29", "LANDSAT_8_2020-12-01", "LANDSAT_8_2020-12-03",
               "LANDSAT_8_2020-12-08", "LANDSAT_8_2020-12-10", "LANDSAT_8_2020-12-14", "LANDSAT_8_2020-12-15",
               "LANDSAT_8_2020-12-21", "LANDSAT_8_2020-12-24", "LANDSAT_8_2020-12-26", "LANDSAT_8_2020-12-30",
               "LANDSAT_8_2021-01-06", "LANDSAT_8_2021-01-13", "LANDSAT_8_2021-01-16", "LANDSAT_8_2021-01-18",
               "LANDSAT_8_2021-01-22", "LANDSAT_8_2021-02-01", "LANDSAT_8_2021-10-31", "LANDSAT_8_2021-11-04",
               "LANDSAT_8_2021-11-09", "LANDSAT_8_2021-11-11", "LANDSAT_8_2021-11-15", "LANDSAT_8_2021-11-20",
               "LANDSAT_8_2021-11-29", "LANDSAT_8_2021-12-01", "LANDSAT_8_2021-12-02", "LANDSAT_8_2021-12-04",
               "LANDSAT_8_2021-12-06", "LANDSAT_8_2021-12-08", "LANDSAT_8_2021-12-11", "LANDSAT_8_2021-12-18",
               "LANDSAT_8_2021-12-20", "LANDSAT_8_2021-12-22", "LANDSAT_8_2021-12-24", "LANDSAT_8_2022-01-05",
               "LANDSAT_8_2022-01-07", "LANDSAT_8_2022-01-12", "LANDSAT_8_2022-01-14", "LANDSAT_8_2022-01-16",
               "LANDSAT_8_2022-01-19", "LANDSAT_8_2022-01-21", "LANDSAT_8_2022-01-25", "LANDSAT_8_2022-01-28",
               "LANDSAT_8_2022-11-07", "LANDSAT_8_2022-11-14", "LANDSAT_8_2022-11-16", "LANDSAT_8_2022-11-18",
               "LANDSAT_8_2022-11-19", "LANDSAT_8_2022-11-21", "LANDSAT_8_2022-11-23", "LANDSAT_8_2022-11-28",
               "LANDSAT_8_2022-12-04", "LANDSAT_8_2022-12-05", "LANDSAT_8_2022-12-11", "LANDSAT_8_2022-12-16",
               "LANDSAT_8_2022-12-18", "LANDSAT_8_2023-01-01", "LANDSAT_8_2023-01-03", "LANDSAT_8_2023-01-10",
               "LANDSAT_8_2023-01-15", "LANDSAT_8_2023-01-22", "LANDSAT_8_2023-01-24", "LANDSAT_8_2023-11-17",
               "LANDSAT_8_2023-11-19", "LANDSAT_8_2023-11-21", "LANDSAT_8_2023-12-05", "LANDSAT_8_2023-12-07",
              # "LANDSAT_8_2023-12-10", # this image is messed up on the GEE side
               "LANDSAT_8_2023-12-19", "LANDSAT_8_2023-12-28", "LANDSAT_8_2023-12-30",
               "LANDSAT_8_2024-01-04", #"LANDSAT_8_2024-01-11", # this image is messed up on the GEE side
               "LANDSAT_8_2024-01-13", "LANDSAT_8_2024-01-22",
               "LANDSAT_8_2024-01-24", "LANDSAT_8_2024-11-03", "LANDSAT_8_2024-11-07", "LANDSAT_8_2024-11-12",
               "LANDSAT_8_2024-11-14", "LANDSAT_8_2024-11-21", #"LANDSAT_8_2024-11-26", # same with this one. Image is there, but it doesn't render under certain zooms on Geemao. 
               "LANDSAT_8_2024-12-09",
               "LANDSAT_8_2024-12-21"])

# Define start and end date for the image collection filter
start_date = "2016-03-06"
end_date = "2025-01-01"

# Define ROI for analysis
roi_for_cropping = ee.Geometry.Rectangle([162.277817, -77.740157, 163.272100, -77.576571])


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



# filter image collection
s2 = ee.ImageCollection('LANDSAT/LC08/C02/T2_TOA')\
    .select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'])\
    .filterDate(start_date, end_date)\
    .map(addImageDate)\
    .filter(ee.Filter.inList("missDate", ids))\
    .filter(ee.Filter.gt('SUN_ELEVATION',20))\
    .filterBounds(roi_for_cropping)\
    .sort('DATE_ACQUIRED')
s3 = mosaic_by_date(s2)

# Clip all the images in the s3 collection down to the ROI
def clip_image(image):
    return image.clip(roi_for_cropping)

# Apply clip to image collection
l8_clipped = s3.map(clip_image)

# Function to calculate mean band values around a simple point
# this function will be passed through the define endmembers 
def calculate_mean_band_values(image, point_geometry):
    buffer = point_geometry.buffer(90)  # 3x3 Landsat pixel window
    band_means = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=buffer,
        scale=30,
        maxPixels=1e6  # Adjusted based on sample size
    )
    return band_means



# Function to define endmembers
def define_endmembers(image, roi, n=1):
    # Calculate brightness
    brightness = image.select(['B2', 'B3', 'B4', 'B5', 'B6']).reduce(ee.Reducer.sum()).rename('brightness')  # RGB and SWIR Bands

    # Generate a grid of points
    points = ee.FeatureCollection.randomPoints(region=roi_LF, points=2000)

    # Calculate brightness for each point
    points_with_brightness = brightness.reduceRegions(
    collection=points,
    reducer=ee.Reducer.mean(),
    scale=20
    )

    # Sort points by brightness
    sorted_points = points_with_brightness.sort('brightness', False)  # Descending order

    # Select the top 3 brightest points
    top_3_brightest = sorted_points.toList(3)
    brightest_geometry = ee.FeatureCollection(top_3_brightest).geometry()

    # Filter out points near the top 3 brightest points
    #filtered_points = points_with_brightness.filterBounds(brightest_geometry.buffer(100)).Not()
    filtered_points = points_with_brightness.filter(ee.Filter.bounds(brightest_geometry.buffer(100)).Not())

    # Sort remaining points in ascending order (dimmest first)
    sorted_filtered_points = filtered_points.sort('brightness', True)

    # Select the bottom 3 dimmest points
    bottom_3_dimmest = sorted_filtered_points.toList(3)
    dimmest_geometry = ee.FeatureCollection(bottom_3_dimmest).geometry()

    # Calculate mean band values for the brightest and dimmest points
    brightest_band_means = calculate_mean_band_values(image, brightest_geometry)
    dimmest_band_means = calculate_mean_band_values(image, dimmest_geometry)

    # Combine into endmembers
    endmembers = ee.List([
    brightest_band_means.values(),
    dimmest_band_means.values()
    ])  
    return endmembers

#print outputs from an example image to see if the outputs are good
example_image = ee.Image('LANDSAT/LC08/C02/T2_TOA/LC08_055116_20231205').select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'])
print(define_endmembers(l8_clipped.first(), roi_LF).getInfo())


def unmix_image_collection(image_collection, roi):
    
    def process_image(image):
        # Define endmembers for the current image
        endmembers = define_endmembers(image, roi)

        # Apply the unmixing process
        unmixed = image.select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']).unmix(endmembers, True, True)

        # Rename unmixed bands for clarity
        unmixed = unmixed.rename(['ice_endmember', 'soil_endmember'])

        # Add properties for tracking
        return unmixed.set('system:time_start', image.get('system:time_start'))

    # Map the unmixing process over the image collection
    unmixed_collection = image_collection.map(process_image)

    return unmixed_collection



