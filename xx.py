# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import io

from google.cloud import speech_v1

BUCKET = os.environ["GOOGLE_CLOUD_TESTS_SPEECH_BUCKET"] or "cloud-samples-tests"

class TestSystemSpeech(object):

    def test_recognize(self):

        client = speech_v1.SpeechClient()

        config = {
            "encoding": speech_v1.enums.RecognitionConfig.AudioEncoding.FLAC,
            "language_code": "en-US",
            "sample_rate_hertz": 16000    
        }

        uri = "gs://{}/speech/broonklyn.flac".format(BUCKET)
        audio = {"uri": uri}

        response = client.recognize(config, audio)
        assert response.error.code == 200


    def test_long_running_recognize(self):

        client = speech_v1.SpeechClient()

        config = speech_v1.types.RecognitionConfig(
            encoding = speech_v1.enums.RecognitionConfig.AudioEncoding.FLAC,
            language_code = "en-US",
            sample_rate_hertz = 16000)

        uri = "gs://{}/speech/broonklyn.flac".format(BUCKET)
        audio = speech_v1.types.RecognitionAudio(uri)
                  
        
        response = client.long_running_recognize(config=config, audio=audio)
        assert response.error.code == 200


    def test_streaming_recognize(self):

        client = speech_v1.SpeechClient()
                  
        config = speech_v1.types.RecognitionConfig(
            encoding = speech_v1.enums.RecognitionConfig.AudioEncoding.FLAC,
            language_code = "en-US",
            sample_rate_hertz = 16000)
        streamingConfig = speech_v1.types.StreamingRecognitionConfig(config = config)

        uri="gs://{}/speech/broonklyn.flac".format(BUCKET)
        with io.open(uri,'rb')as stream:
            requests = [speech_v1.types.StreamingRecognizeRequest(
                 audio_content=stream.read()
            )]
        
        response = client.streaming_recognize(streamingConfig, requests)
        assert response.error.code == 200    


        gcs = storage.Client()
        gcs_bucket = gcs.get_bucket(BUCKET)
 
        file_name = "speech/brooklyn.flac"
        blob = gcs_bucket.blob(file_name)
        file_as_string = blob.download_as_string()
        
        client = speech_v1.SpeechClient()
                  
        config = speech_v1.types.RecognitionConfig(
            encoding = speech_v1.enums.RecognitionConfig.AudioEncoding.FLAC,
            language_code = "en-US",
            sample_rate_hertz = 16000)
        streamingConfig = speech_v1.types.StreamingRecognitionConfig(config = config)

        requests = [speech_v1.types.StreamingRecognizeRequest(
            audio_content=io.BytesIO(file_as_string)
        )]
        
        responses = client.streaming_recognize(streamingConfig, requests)
        assert len(responses)>0






        try:
            BUCKET = os.environ["GOOGLE_CLOUD_TESTS_SPEECH_BUCKET"]
        except KeyError:
            BUCKET = "cloud-samples-tests"

        client = speech_v1.SpeechClient()
                  
        config = speech_v1.types.RecognitionConfig(
            encoding = speech_v1.enums.RecognitionConfig.AudioEncoding.FLAC,
            language_code = "en-US",
            sample_rate_hertz = 16000)
        streamingConfig = speech_v1.types.StreamingRecognitionConfig(config = config)

        uri = "https://storage.googleapis.com/{}/speech/brooklyn.flac".format(BUCKET)

        requests = [speech_v1.types.StreamingRecognizeRequest(
              audio_content=retrieve.get(uri).content
        )]
        
        responses = client.streaming_recognize(streamingConfig, requests)

        for response in responses:
            for result in response.results:
                print(result.alternatives[0].transcript)

        
