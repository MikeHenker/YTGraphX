"""
YouTube Data API v3 Integration
Handles all YouTube API interactions for channel data retrieval
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

from config import YOUTUBE_API_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, HISTORICAL_MONTHS


class YouTubeAPI:
    """YouTube Data API v3 wrapper class"""
    
    def __init__(self, api_key: str):
        """Initialize YouTube API client"""
        self.api_key = api_key
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)
    
    def get_channel_info(self, channel_identifier: str) -> Dict:
        """
        Get channel information by channel ID or username
        
        Args:
            channel_identifier: Channel ID or username (with or without @)
            
        Returns:
            Dictionary containing channel information
        """
        try:
            # Remove @ if present
            if channel_identifier.startswith('@'):
                channel_identifier = channel_identifier[1:]
            
            # Try to get channel by ID first
            try:
                request = self.youtube.channels().list(
                    part='snippet,statistics,brandingSettings',
                    id=channel_identifier
                )
                response = request.execute()
                
                if 'items' in response and response['items']:
                    return self._format_channel_data(response['items'][0])
            except Exception as e:
                pass
            
            # If not found by ID, try to get by username
            try:
                request = self.youtube.channels().list(
                    part='snippet,statistics,brandingSettings',
                    forUsername=channel_identifier
                )
                response = request.execute()
                
                if 'items' in response and response['items']:
                    return self._format_channel_data(response['items'][0])
            except Exception as e:
                pass
            
            # If both methods failed, try searching by channel name
            try:
                search_request = self.youtube.search().list(
                    part='snippet',
                    q=channel_identifier,
                    type='channel',
                    maxResults=1
                )
                search_response = search_request.execute()
                
                if 'items' in search_response and search_response['items']:
                    channel_id = search_response['items'][0]['id']['channelId']
                    
                    # Get detailed channel info
                    channel_request = self.youtube.channels().list(
                        part='snippet,statistics,brandingSettings',
                        id=channel_id
                    )
                    channel_response = channel_request.execute()
                    
                    if 'items' in channel_response and channel_response['items']:
                        return self._format_channel_data(channel_response['items'][0])
            except Exception as e:
                pass
            
            raise ValueError(f"Channel '{channel_identifier}' not found. Please check the channel ID or username.")
            
        except HttpError as e:
            if e.resp.status == 403:
                raise ValueError("API quota exceeded or invalid API key. Please check your API key and quota.")
            elif e.resp.status == 404:
                raise ValueError(f"Channel '{channel_identifier}' not found")
            else:
                raise ValueError(f"API Error: {e}")
        except Exception as e:
            raise ValueError(f"Error fetching channel info: {str(e)}")
    
    def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict]:
        """
        Get recent videos from a channel
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to retrieve
            
        Returns:
            List of video dictionaries
        """
        try:
            # Get uploads playlist ID
            channel_request = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            )
            channel_response = channel_request.execute()
            
            if not channel_response['items']:
                raise ValueError("Channel not found")
            
            uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            videos_request = self.youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=max_results
            )
            videos_response = videos_request.execute()
            
            # Get detailed video statistics
            video_ids = [item['contentDetails']['videoId'] for item in videos_response['items']]
            
            if not video_ids:
                return []
            
            # Get video details
            video_details_request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            )
            video_details_response = video_details_request.execute()
            
            return [self._format_video_data(video) for video in video_details_response['items']]
            
        except HttpError as e:
            raise ValueError(f"Error fetching videos: {e}")
        except Exception as e:
            raise ValueError(f"Error fetching videos: {str(e)}")
    
    def _format_channel_data(self, channel_data: Dict) -> Dict:
        """Format raw channel data from API"""
        return {
            'id': channel_data['id'],
            'title': channel_data['snippet']['title'],
            'description': channel_data['snippet']['description'],
            'custom_url': channel_data['snippet'].get('customUrl', ''),
            'published_at': channel_data['snippet']['publishedAt'],
            'thumbnails': channel_data['snippet']['thumbnails'],
            'statistics': channel_data['statistics'],
            'branding_settings': channel_data.get('brandingSettings', {}),
            'subscriber_count': int(channel_data['statistics'].get('subscriberCount', 0)),
            'view_count': int(channel_data['statistics'].get('viewCount', 0)),
            'video_count': int(channel_data['statistics'].get('videoCount', 0))
        }
    
    def _format_video_data(self, video_data: Dict) -> Dict:
        """Format raw video data from API"""
        return {
            'id': video_data['id'],
            'title': video_data['snippet']['title'],
            'description': video_data['snippet']['description'],
            'published_at': video_data['snippet']['publishedAt'],
            'thumbnails': video_data['snippet']['thumbnails'],
            'statistics': video_data['statistics'],
            'duration': video_data['contentDetails']['duration'],
            'view_count': int(video_data['statistics'].get('viewCount', 0)),
            'like_count': int(video_data['statistics'].get('likeCount', 0)),
            'comment_count': int(video_data['statistics'].get('commentCount', 0))
        }
    
    def generate_historical_data(self, channel_data: Dict) -> Dict[str, List[Dict]]:
        """
        Generate mock historical data for demonstration purposes
        
        Args:
            channel_data: Channel information dictionary
            
        Returns:
            Dictionary containing historical data for subscribers, views, and videos
        """
        current_subscribers = channel_data['subscriber_count']
        current_views = channel_data['view_count']
        current_videos = channel_data['video_count']
        
        subscriber_history = []
        view_history = []
        video_history = []
        
        # Generate historical data for the specified number of months
        for i in range(HISTORICAL_MONTHS, 0, -1):
            date = datetime.now() - timedelta(days=30 * i)
            date_str = date.strftime('%Y-%m-%d')
            
            # Simulate growth patterns with some randomness
            growth_factor = 1 - (i * 0.05)  # 5% growth per month
            random_variation = 0.8 + random.random() * 0.4  # ±20% variation
            
            subscriber_history.append({
                'date': date_str,
                'subscribers': int(current_subscribers * growth_factor * random_variation)
            })
            
            view_history.append({
                'date': date_str,
                'views': int(current_views * growth_factor * random_variation)
            })
            
            video_history.append({
                'date': date_str,
                'videos': int(current_videos * growth_factor * random_variation)
            })
        
        return {
            'subscriber_history': subscriber_history,
            'view_history': view_history,
            'video_history': video_history
        }
    
    def get_comprehensive_stats(self, channel_identifier: str) -> Dict:
        """
        Get comprehensive channel statistics including historical data
        
        Args:
            channel_identifier: Channel ID or username
            
        Returns:
            Dictionary containing all channel statistics and historical data
        """
        try:
            # Get channel information
            channel_data = self.get_channel_info(channel_identifier)
            
            # Get recent videos
            videos = self.get_channel_videos(channel_data['id'])
            
            # Generate historical data
            historical_data = self.generate_historical_data(channel_data)
            
            return {
                'channel': channel_data,
                'videos': videos,
                **historical_data
            }
            
        except Exception as e:
            raise ValueError(f"Error getting comprehensive stats: {str(e)}")


# Create global instance
youtube_api = YouTubeAPI(YOUTUBE_API_KEY)
