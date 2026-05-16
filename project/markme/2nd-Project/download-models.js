import fs from 'fs';
import https from 'https';
import path from 'path';

const modelsDir = path.join(process.cwd(), 'public', 'models');
if (!fs.existsSync(modelsDir)) {
  fs.mkdirSync(modelsDir, { recursive: true });
}

const baseUrl = 'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/';
const files = [
  'tiny_face_detector_model-shard1',
  'tiny_face_detector_model-weights_manifest.json',
  'face_landmark_68_model-shard1',
  'face_landmark_68_model-weights_manifest.json',
  'face_recognition_model-shard1',
  'face_recognition_model-shard2',
  'face_recognition_model-weights_manifest.json'
];

files.forEach(file => {
  const dest = path.join(modelsDir, file);
  https.get(baseUrl + file, (response) => {
    const fileStream = fs.createWriteStream(dest);
    response.pipe(fileStream);
    fileStream.on('finish', () => {
      fileStream.close();
      console.log('Downloaded', file);
    });
  }).on('error', (err) => {
    console.error('Error downloading', file, err.message);
  });
});
