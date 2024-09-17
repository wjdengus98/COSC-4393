from dip import *

class ShapeCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes as input:
        image: binary image
        return: a list/dict of regions
        """
        new_image = [[0] * len(image[0]) for _ in range(len(image))] #2D Array with everything black
        k = 1 #region number
        regions = dict()

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i][j] != 0.:  # Assuming 255 is the foreground
                    left = new_image[i][j - 1] if j > 0 else 0
                    top =  new_image[i - 1][j] if i > 0 else 0

                    if image[i][j-1] == 0 and image[i-1][j] == 0: #both black
                        new_image[i][j] = k
                        regions[k] = [(i, j)]
                        k += 1
                    elif image[i][j-1] != 0 and image[i-1][j] == 0: #left is 1 and top is black
                        new_image[i][j] = left
                        regions[left].append((i, j))
                    elif image[i][j-1]  == 0 and image[i-1][j] != 0:# left is 0 and top is 255
                        new_image[i][j] = top
                        regions[top].append((i, j))
                    elif image[i][j-1] != 0 and image[i-1][j] != 0:
                        new_image[i][j] = left  # Assign one of the labels; here we choose left
                        regions[left].append((i, j))
                        if left != top:
                            # Merge regions if necessary
                            regions[top].extend(regions[left])
                            # Update all coordinates in new_image that have the old label
                            for coords in regions[left]:
                                new_image[coords[0]][coords[1]] = top
                                regions[top].append(coords)
                            del regions[left]  # Remove the old label



        return regions

    def identify_shapes(self, region):
        """Compute shape features area and centroid, and shape
        Ignore shapes smaller than 10 pixels in area.
        takes as input
        region: a list/dict of pixels in a region
        returns: shapes, a data structure with centroid, area, and shape (c, s, r, or e) for each region
        c - circle, s - squares, r - rectangle, and e - ellipse
        """

        # Please print your shape statistics to stdout, one line for each shape
        # Region: <region_no>, centroid: <centroid>, area: <shape area>, shape: <shape type>
        # Example: Region: 871, centroid: (969.11, 51.11), area: 707, shape: c
        shapes = dict()
        for region_no, pixels in region.items():
            if len(pixels) < 10:
                continue

            # Initialize minimum and maximum coordinates to infinity
            min_x = min_y = float('inf')
            max_x = max_y = -float('inf')

            # Iterate through each pixel in the region to find the bounding box
            for x, y in pixels:
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y

            # Calculate the width and height and area
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            area = len(pixels)

            # Calculate the centroid
            centroid_x = sum(x for x, y in pixels) / len(pixels)
            centroid_y = sum(y for x, y in pixels) / len(pixels)
            centroid = (centroid_x, centroid_y)

            # Calculate the aspect ratio of the shape
            aspect_ratio = max([width, height]) / min([width, height])
            fill_ratio = area / (width * height)

            # Determine the shape type based on aspect ratio and fill ratio: I guess ratio of error: +5% or -5% estimation
            if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                shape_type = 's' if fill_ratio > 0.95 else 'c'
            else:
                shape_type = 'r' if fill_ratio > 0.95 else 'e'

            shapes[region_no] = {'centroid': centroid, 'area': area, 'shape': shape_type}

        return shapes

    def count_shapes(self, shapes_data):
        """Compute the count of shapes using the shapes data returned from identify shapes function
           takes as input
           shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
           returns: a dictionary with count of each shape
           Example return value: {'circles': 21, 'ellipses': 25, 'rectangles': 31, 'squares': 23}
           """
        shape_counts = {"circles": 0, "ellipses": 0, "rectangles": 0, "squares": 0}

        for shape_info in shapes_data.values():

            shape_type = shape_info['shape']

            # Increment the count for the corresponding shape type
            if shape_type == 'c':
                shape_counts["circles"] += 1
            elif shape_type == 'e':
                shape_counts["ellipses"] += 1
            elif shape_type == 'r':
                shape_counts["rectangles"] += 1
            elif shape_type == 's':
                shape_counts["squares"] += 1

        return shape_counts

    def mark_image_regions(self, image, shapes_data):
        """Creates a new image with computed stats for each shape
        Make a copy of the image on which you can write text.
        takes as input
        image: binary image
        shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
        returns: image marked with center and shape_type"""
        final_image = image.copy()

        for _, shape in shapes_data.items():
            # Extract the centroid coordinates and the shape type
            centroid = (int(shape['centroid'][1]), int(shape['centroid'][0]))
            shape_type = shape['shape']

            putText(final_image,shape_type,centroid,FONT_HERSHEY_SIMPLEX,
                        0.7,(0,0,0),1,LINE_AA)

        return final_image
