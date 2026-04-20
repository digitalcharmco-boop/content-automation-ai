#!/usr/bin/env python3
"""
Publishing and Promotion Automation
Handles uploading to YouTube and cross-posting to social media platforms.
Requires explicit human approval before publishing.
"""

import os
import json
from pathlib import Path
from datetime import datetime
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class ContentPublisher:
    def __init__(self):
        self.youtube_scopes = ['https://www.googleapis.com/auth/youtube.upload']
        self.credentials_file = 'credentials.json'
        self.token_file = 'token.json'
        self.pending_dir = Path('pending_uploads')
        self.pending_dir.mkdir(exist_ok=True)
    
    def prepare_upload(self, video_file, metadata=None):
        """Prepare video for upload with human approval required"""
        video_path = Path(video_file)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")
        
        # Load video metadata
        metadata_file = video_path.with_suffix('.json')
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                video_metadata = json.load(f)
        else:
            video_metadata = {}
        
        # Prepare upload package
        upload_data = {
            "video_file": str(video_file),
            "metadata": metadata or video_metadata,
            "created_at": datetime.now().isoformat(),
            "status": "pending_approval",
            "approved": False
        }
        
        # Generate upload package filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_file = self.pending_dir / f"upload_package_{timestamp}.json"
        
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(upload_data, f, indent=2)
        
        print(f"Upload package created: {package_file}")
        print("HUMAN APPROVAL REQUIRED: Review and approve before publishing")
        return str(package_file)
    
    def approve_upload(self, package_file):
        """Mark upload package as approved"""
        with open(package_file, 'r', encoding='utf-8') as f:
            upload_data = json.load(f)
        
        upload_data['approved'] = True
        upload_data['approved_at'] = datetime.now().isoformat()
        
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(upload_data, f, indent=2)
        
        print(f"Upload approved: {package_file}")
        return upload_data
    
    def authenticate_youtube(self):
        """Authenticate with YouTube API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.youtube_scopes)
        
        # Refresh or get new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"YouTube credentials file not found: {self.credentials_file}\n"
                        "Download from Google Cloud Console and place in current directory"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.youtube_scopes
                )
                creds = flow.run_local_server(port=0)
            
            # Save token
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        return build('youtube', 'v3', credentials=creds)
    
    def upload_to_youtube(self, package_file):
        """Upload approved video to YouTube"""
        with open(package_file, 'r', encoding='utf-8') as f:
            upload_data = json.load(f)
        
        if not upload_data.get('approved', False):
            raise ValueError("Upload must be approved before publishing")
        
        video_file = upload_data['video_file']
        metadata = upload_data.get('metadata', {})
        
        # Authenticate
        youtube = self.authenticate_youtube()
        
        # Prepare upload parameters
        title = metadata.get('topic', 'Automated Upload')
        description = metadata.get('description', 'Generated content')
        tags = metadata.get('tags', [])
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'private'  # Start as private for safety
            }
        }
        
        # Upload video
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        
        print(f"Uploading video: {title}")
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")
        
        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Update package with results
        upload_data['youtube_video_id'] = video_id
        upload_data['youtube_url'] = video_url
        upload_data['uploaded_at'] = datetime.now().isoformat()
        upload_data['status'] = 'uploaded'
        
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(upload_data, f, indent=2)
        
        print(f"Video uploaded successfully: {video_url}")
        return upload_data
    
    def cross_post_social_media(self, upload_data):
        """Cross-post to social media platforms"""
        video_url = upload_data.get('youtube_url')
        title = upload_data.get('metadata', {}).get('topic', 'New Video')
        
        if not video_url:
            print("No YouTube URL found for cross-posting")
            return
        
        # Prepare social media posts
        social_posts = {
            'twitter': f"New video: {title} {video_url} #YouTube",
            'facebook': f"Check out my new video: {title}\n{video_url}",
            'linkedin': f"New content published: {title}\n{video_url}"
        }
        
        # Save posts for manual posting (or integrate with social media APIs)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        posts_file = f"social_posts_{timestamp}.json"
        
        with open(posts_file, 'w', encoding='utf-8') as f:
            json.dump(social_posts, f, indent=2)
        
        print(f"Social media posts prepared: {posts_file}")
        print("Note: Manual posting or API integration required for actual posting")
        
        return posts_file
    
    def publish_content(self, package_file):
        """Complete publishing workflow"""
        print(f"Starting publishing workflow: {package_file}")
        
        # Upload to YouTube
        upload_result = self.upload_to_youtube(package_file)
        
        # Cross-post to social media
        social_posts_file = self.cross_post_social_media(upload_result)
        
        # Generate analytics tracking
        analytics_data = {
            'video_id': upload_result.get('youtube_video_id'),
            'video_url': upload_result.get('youtube_url'),
            'published_at': datetime.now().isoformat(),
            'social_posts': social_posts_file,
            'tracking_enabled': True
        }
        
        analytics_file = f"analytics_{upload_result.get('youtube_video_id', 'unknown')}.json"
        with open(analytics_file, 'w', encoding='utf-8') as f:
            json.dump(analytics_data, f, indent=2)
        
        print("Publishing workflow complete!")
        print(f"YouTube: {upload_result.get('youtube_url')}")
        print(f"Social posts: {social_posts_file}")
        print(f"Analytics: {analytics_file}")
        
        return {
            'youtube_result': upload_result,
            'social_posts': social_posts_file,
            'analytics': analytics_file
        }

def main():
    """Interactive publishing workflow"""
    publisher = ContentPublisher()
    
    action = input("Choose action (prepare/approve/publish): ").lower()
    
    if action == 'prepare':
        video_file = input("Enter path to video file: ")
        package_file = publisher.prepare_upload(video_file)
        print(f"Review the upload package and approve when ready:")
        print(f"python publisher.py approve {package_file}")
    
    elif action == 'approve':
        package_file = input("Enter path to upload package: ")
        publisher.approve_upload(package_file)
    
    elif action == 'publish':
        package_file = input("Enter path to approved package: ")
        try:
            result = publisher.publish_content(package_file)
            print("Publishing completed successfully!")
        except Exception as e:
            print(f"Publishing failed: {str(e)}")
    
    else:
        print("Invalid action. Use: prepare, approve, or publish")

if __name__ == "__main__":
    main()