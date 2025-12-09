# Q2 - Programming Style (PEP 8 guidelines)
# Lab: Demonstrate indentation, comments,
#      and variables following PEP 8

def calculate_area_of_rectangle(width, height):
    """
    Calculate area of a rectangle.

    Args:
        width (float): width of the rectangle
        height (float): height of the rectangle

    Returns:
        float: area of the rectangle
    """
    area = width * height  # area = w × h
    return area


# main block (example of clear structure and names)
if __name__ == "__main__":
    # Using snake_case variable names and proper spacing
    rect_width = 5.0
    rect_height = 3.0

    # Comment explaining what we are doing
    result_area = calculate_area_of_rectangle(rect_width, rect_height)
    print("Area of rectangle:", result_area)
