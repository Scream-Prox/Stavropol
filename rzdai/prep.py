import os
import cv2
import re
from PIL import Image, ImageDraw, ImageFont
import torch
from torchvision.models import resnext101_32x8d
from torchvision import transforms
import torch.nn as nn
from collections import Counter

def process_video(video_path):
    def extract_frames(video_path):
        frames_folder = os.path.splitext(video_path)[0] + '_frames'
        os.makedirs(frames_folder, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % 5 == 0:
                frame_filename = os.path.join(frames_folder, f'frame_{frame_count:04d}.jpg')
                cv2.imwrite(frame_filename, frame)

            frame_count += 1

        cap.release()

        return frames_folder

    def predict_and_draw(frames_folder, model, device):
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        image_paths = [os.path.join(frames_folder, image_name) for image_name in os.listdir(frames_folder)]
        images = [transform(Image.open(image_path)) for image_path in image_paths]

        images = [image.to(device) for image in images]

        predicted_labels = []

        model.eval()

        output_dir = 'predicted'
        os.makedirs(output_dir, exist_ok=True)

        prev_predicted_label = None

        predicted_labels = []

        for i, (image_path, image) in enumerate(zip(image_paths, images)):
            predicted_label = None
            with torch.no_grad():
                output = model(image.unsqueeze(0))
                _, predicted = output.max(1)
                predicted_label = predicted.item()
                predicted_labels.append(predicted_label)
                
            print(f"Фотография: {os.path.basename(image_path)}, Предсказанная метка: {predicted_label}")

            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("Arial.ttf", size=60)
            x, y = 20, 20
            text_color = (255, 255, 255)
            draw.text((x, y), str(predicted_label), fill=text_color, font=font)
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            img.save(output_path)

        
        most_common_label = Counter(predicted_labels).most_common(1)[0][0]
        print(f"Наиболее частая метка: {most_common_label}")

        return most_common_label

    video_folder = extract_frames(video_path)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = resnext101_32x8d().to(device=device)
    model.fc = nn.Linear(model.fc.in_features, 24)
    checkpoint = torch.load('best_final_class_resnext101_32x8d.pth', map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    frames_folder = extract_frames(video_folder)
    most_common_label = predict_and_draw(video_folder, model, device)
    print(most_common_label)

    return most_common_label