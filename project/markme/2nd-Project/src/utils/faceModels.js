import * as faceapi from 'face-api.js'

let loadPromise = null

export async function ensureFaceModelsLoaded() {
  if (faceapi.nets.tinyFaceDetector.isLoaded && faceapi.nets.faceLandmark68Net.isLoaded && faceapi.nets.faceRecognitionNet.isLoaded) {
    return true
  }

  if (!loadPromise) {
    loadPromise = Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
      faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
      faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
    ])
      .then(() => true)
      .catch((error) => {
        loadPromise = null
        throw error
      })
  }

  await loadPromise
  return true
}
