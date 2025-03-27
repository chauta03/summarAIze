from sqlalchemy.ext.asyncio import AsyncSession
from azure.storage.blob import BlobServiceClient
from fastapi import UploadFile, File
import os


class StorageService:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))

    def upload_video(self, file: UploadFile = File(...)):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=os.getenv("CONTAINER_NAME"), blob=file.filename)

            # Upload file to Azure Blob Storage
            with file.file as f:
                blob_client.upload_blob(f, overwrite=True)

            return {"message": "Video uploaded successfully", "video_url": blob_client.url}

        except Exception as e:
            return {"error": str(e)}

    
    def delete_video(self, filename: str):
        blob_client = self.blob_service_client.get_blob_client(container=os.getenv("CONTAINER_NAME"), blob=filename)
        blob_client.delete_blob()
        return {"message": "Video deleted successfully"}

    def list_videos(self):
        container_client = self.blob_service_client.get_container_client(os.getenv("CONTAINER_NAME"))
        blob_list = container_client.list_blobs()
        videos = []
        
        # Get the container URL
        container_url = container_client.url
        
        for blob in blob_list:
            # Construct the full blob URL using the container URL and blob name
            video_url = f"{container_url}/{blob.name}"
            videos.append({"name": blob.name, "url": video_url})
        
        return videos


    def get_video(self, filename: str):
        blob_client = self.blob_service_client.get_blob_client(container=os.getenv("CONTAINER_NAME"), blob=filename)
        return {"video_url": blob_client.url}
