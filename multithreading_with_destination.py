import os
import cv2
import shutil
import logging
from typing import Generator
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ImageResizer:
    def __init__(self, source_dir: str, destination_dir: str = None, target_file_size_mb: int = 1, num_threads: int = 4):
        self.source_dir = source_dir
        # Determine the base name of the source directory
        base_source_dir_name = os.path.basename(source_dir)
        # If destination_dir is provided, append the source directory name with '_low_res' inside destination_dir
        if destination_dir:
            self.destination_dir = os.path.join(destination_dir, f"{base_source_dir_name}_low_res")
        else:
            # If no destination_dir is provided, create a '_low_res' directory alongside the source_dir
            self.destination_dir = f"{source_dir}_low_res"
        
        self.target_file_size_bytes = target_file_size_mb * 1024 * 1024
        self.num_threads = num_threads
        self.image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

    def get_image_paths(self) -> Generator[str, None, None]:
        for root, _, files in os.walk(self.source_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in self.image_extensions):
                    yield os.path.join(root, file)

    def resize_images_multithreaded(self):
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            list(executor.map(self.resize_image, self.get_image_paths()))

    def resize_image(self, image_path: str):
        relative_path = os.path.relpath(image_path, self.source_dir)
        output_dir = os.path.join(self.destination_dir, os.path.dirname(relative_path))
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(image_path))

        if os.path.exists(output_path):
            logging.info(f"File {os.path.basename(image_path)} already exists in output folder. Skipping...")
            return

        file_size_bytes = os.path.getsize(image_path)
        if file_size_bytes <= self.target_file_size_bytes:
            logging.info(f"{os.path.basename(image_path)} is less than {self.target_file_size_bytes // 1024 // 1024}MB, copying without resizing.")
            shutil.copy(image_path, output_dir)
            return

        logging.info(f"Resizing {os.path.basename(image_path)}")
        try:
            image = cv2.imread(image_path)
            reduction_percentage = self.calculate_reduction_percentage(image, image_path)
            resized_image = self.resize_image_percentage(image, percentage=100 - reduction_percentage)
            self.save_image(resized_image, output_path)
        except Exception as e:
            logging.error(f"Failed to process image: {os.path.basename(image_path)}. Error: {e}")

    def save_image(self, image, file_path):
        cv2.imwrite(file_path, image)
        logging.info(f"Saved image to {file_path}")

    def resize_image_percentage(self, image, percentage):
        ratio = percentage / 100.0
        dim = (int(image.shape[1] * ratio), int(image.shape[0] * ratio))
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    def calculate_reduction_percentage(self, image, image_path):
        left, right = 0, 100
        best_reduction = 0
        while left <= right:
            mid = (left + right) // 2
            resized_image = self.resize_image_percentage(image, percentage=100 - mid)
            extension = os.path.splitext(image_path)[1].lower()

            size_bytes = cv2.imencode(extension, resized_image)[1].size

            if size_bytes > self.target_file_size_bytes:
                left = mid + 1
            else:
                best_reduction = mid
                right = mid - 1
        return best_reduction


if __name__ == "__main__":
    source_dir = "C:\\Users\\Username\\Downloads"
    # This can be modified to any destination directory, '_low_res' suffix will be automatically added
    destination_dir = "C:\\Users\\Username\\Downloads\\Resized_Image"
    resizer = ImageResizer(source_dir, destination_dir, target_file_size_mb=1, num_threads=3)
    resizer.resize_images_multithreaded()
