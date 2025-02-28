##### East Lobe SMA workflow
# iniialize and load packages
import ee
import geemap

# Initialize Earth Engine
ee.Authenticate()
ee.Initialize()

# define ROIs
roi_EL = ee.Geometry.Polygon([
    [162.7492465962224,-77.6442206115621],
    [162.76143455398608,-77.64311859255932],
    [162.76915931594897,-77.6430451211855],
    [162.78598213089037,-77.64058358163193],
    [162.7990283955388,-77.63915052291087],
    [162.81018638504077,-77.63870954885815],
    [162.8232326496892,-77.6378275542914],
    [162.83730888259936,-77.63801130826822],
    [162.84692191970873,-77.63672497396273],
    [162.86477470291186,-77.63315930165008],
    [162.86889457595873,-77.63143124067741],
    [162.87799262893725,-77.63065905149807],
    [162.87833595169116,-77.6320563114462],
    [162.89876365554858,-77.63201954343829],
    [162.91144034988244,-77.63315930165008],
    [162.92105338699182,-77.63220338240187],
    [162.93839118606408,-77.63257105225898],
    [162.91847846633752,-77.62852609197509],
    [162.9152169001754,-77.62650312348197],
    [162.90732047683557,-77.623523249673],
    [162.85805366165002,-77.62922485996916],
    [162.83264777786096,-77.63371076043876],
    [162.81908652908166,-77.63536499156395],
    [162.8130783808883,-77.63554878157487],
    [162.78973243362267,-77.63804805874092],
    [162.78200767165978,-77.63962822732537],
    [162.77153632766564,-77.6409142642629],
    [162.74595878249963,-77.64286144086948],
    [162.7492465962224,-77.6442206115621]
    ])

roi_EL_crop = ee.Geometry.Polygon([[162.76086531075168,-77.65942105902757],
                                   [162.97372541817356,-77.63628638137197],
                                   [162.92360029610325,-77.61531822019396],
                                   [162.70902357491184,-77.63885900807094],
                                   [162.76086531075168,-77.65942105902757]
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
roi_for_cropping = ee.Geometry.Polygon([[162.76086531075168,-77.65942105902757],
                                   [162.97372541817356,-77.63628638137197],
                                   [162.92360029610325,-77.61531822019396],
                                   [162.70902357491184,-77.63885900807094],
                                   [162.76086531075168,-77.65942105902757]
])

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
    points = ee.FeatureCollection.randomPoints(region=roi_LH, points=2000)

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
print(define_endmembers(l8_clipped.first(), roi_LH).getInfo())


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

# apply process to all images in collection
output_collection = unmix_image_collection(image_collection = l8_clipped, roi = roi_LH)
#result_collection = l8_clipped.map(unmix_image_collection(roi_for_brightness))
print(output_collection.getInfo())



# export the images in the unmixed collection
def export_image(image):
    date_str = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd').getInfo()
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=f'unmixed_images_{date_str}',
        folder='EarthEngine',  # Replace with your folder name
        scale=30,                 # Define the scale (e.g., 30 meters per pixel)
        crs='EPSG:3031',          # Define the Coordinate Reference System
        region=pointed,  # Define the region to export
        fileNamePrefix=f'LANDSAT_unmix_feb28_{date_str}'
    )
    task.start()
    print(f"Export started for image with date {date_str}.")


    # need to make sure the unmixed collection is called here, not the l8_clipped variable. 
def process_images():
    image_list = output_collection.toList(output_collection.size().getInfo())
    num_images = image_list.size().getInfo()
    
    for i in range(num_images):
        image = ee.Image(image_list.get(i))
        export_image(image)

process_images()