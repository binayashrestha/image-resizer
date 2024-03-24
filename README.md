
# Multithreaded Image Resizer with EXIF Optimization

This Python script utilizes multithreading to efficiently resize images in a directory while optimizing them to a target file size and preserving EXIF metadata. It is especially useful for bulk image processing tasks, ensuring that the resized images retain their original quality and EXIF information as much as possible.

## Features

- **Multithreading Support**: Leverages Python's `concurrent.futures.ThreadPoolExecutor` for concurrent image processing, significantly speeding up the resizing process for large numbers of images.
- **EXIF Data Preservation**: Utilizes PIL (Python Imaging Library) to maintain EXIF data during the resizing process, ensuring that metadata like camera settings, GPS data, and timestamps are preserved.
- **Flexible File Size Targeting**: Allows specifying a target file size for the resized images, automatically adjusting the resizing percentage to meet this criterion.
- **Wide Format Support**: Supports resizing of various image formats including JPG, JPEG, PNG, BMP, and TIFF.

## Requirements

- Python 3.x
- OpenCV-Python (`opencv-python`)
- Pillow (`Pillow`)
- NumPy (`numpy`)

## Setup

1. Ensure you have Python 3.x installed on your system.
2. Install the required Python packages:

```sh
pip install opencv-python Pillow numpy
```

3. Clone this repository or download the `multithreading_exif_optimized.py` script directly.

## Usage

1. Modify the `source_dir` and `destination_dir` paths in the `if __name__ == "__main__"` section of the script to point to your source and destination directories, respectively.
2. Optionally, adjust the `target_file_size_mb` and `num_threads` parameters to fit your needs.
3. Run the script:

```sh
python multithreading_exif_optimized.py
```

## How It Works

- The script scans the `source_dir` for image files.
- For each image, it calculates the necessary reduction percentage to meet the specified target file size while preserving as much quality as possible.
- Images are then resized and saved to the `destination_dir`, with their EXIF data intact.

## Contributing

Contributions to improve the script are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This script is provided under the MIT License. See the LICENSE file for more details.
