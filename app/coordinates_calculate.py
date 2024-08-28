# Description: This script calculates the real-world coordinates of a tracking point in meters, the azimuth angle to the zero point in degrees,
# and the distance to the zero point in meters. The script also calculates the resulting relative drone azimuth to the zero point in degrees.
# The script uses the camera's field of view, resolution, and the distance from the camera to the tracking point as input parameters.
import math

DIAGONAL_CAMERA_FOV = 55  # Field of view in degrees
RESOLUTION_WIDTH = 720  # Width of the camera resolution in pixels
RESOLUTION_HEIGHT = 1280  # Height of the camera resolution in pixels

def calculate_real_coordinates(pixel_x, pixel_y, attitude):
    global DIAGONAL_CAMERA_FOV, RESOLUTION_WIDTH, RESOLUTION_HEIGHT

    # Convert diagonal FOV from degrees to radians
    diagonal_fov_rad = math.radians(DIAGONAL_CAMERA_FOV)
    
    # Calculate the aspect ratio
    aspect_ratio = RESOLUTION_WIDTH / RESOLUTION_HEIGHT
    
    # Calculate the horizontal and vertical FOVs
    horizontal_fov_rad = 2 * math.atan(math.tan(diagonal_fov_rad / 2) / math.sqrt(1 + aspect_ratio**2))
    vertical_fov_rad = 2 * math.atan(math.tan(diagonal_fov_rad / 2) / math.sqrt(1 + (1 / aspect_ratio)**2))
    
    # Calculate the angle per pixel
    angle_per_pixel_x = horizontal_fov_rad / RESOLUTION_WIDTH
    angle_per_pixel_y = vertical_fov_rad / RESOLUTION_HEIGHT
    
    # Calculate the angles in the horizontal and vertical directions
    angle_x = pixel_x * angle_per_pixel_x
    angle_y = pixel_y * angle_per_pixel_y
    
    # Calculate the real-world coordinates
    real_x = round(attitude * math.tan(angle_x), 2)
    real_y = round(attitude * math.tan(angle_y), 2)
    
    return real_x, real_y

def calculate_azimuth_and_distance(real_x, real_y):
    # Calculate the distance using the Pythagorean theorem
    distance = math.sqrt(real_x**2 + real_y**2)
    
    # Calculate the azimuth angle in radians
    azimuth_rad = math.atan2(real_x, real_y)  # Note the order of arguments
    
    # Convert the azimuth angle to degrees
    azimuth_deg = math.degrees(azimuth_rad) - 180
    
    # Adjust the azimuth to be in the range [0, 360] degrees
    if azimuth_deg < 0:
        azimuth_deg += 360
    
    return round(azimuth_deg, 2), round(distance, 2)

def calculate_resulting_azimuth(drone_azimuth, target_azimuth):
    # Calculate the resulting azimuth
    resulting_azimuth = target_azimuth - drone_azimuth
    
    # Adjust the resulting azimuth to be in the range [0, 360] degrees
    if resulting_azimuth < 0:
        resulting_azimuth += 360
    elif resulting_azimuth >= 360:
        resulting_azimuth -= 360
    
    return round(resulting_azimuth, 2)

def main():
    # Example usage
    x = -100  # x-coordinate of the tracking point in pixels
    y = 180  # y-coordinate of the tracking point in pixels
    attitude = 30  # Distance from the camera to the tracking point in meters
    drone_azimuth = 90  # Azimuth angle of the drone in degrees

    real_x, real_y = calculate_real_coordinates(x, y, attitude)
    print(f"Real coordinates: ({real_x}, {real_y}) meters")

    azimuth, distance = calculate_azimuth_and_distance(real_x, real_y)
    print(f"Azimuth to the zero point: {azimuth} degrees, distance: {distance} meters")

    resulting_azimuth = calculate_resulting_azimuth(drone_azimuth, azimuth)
    print(f"Resulting relative drone azimuth to the zero point: {resulting_azimuth} degrees")

if __name__ == "__main__":
    main()