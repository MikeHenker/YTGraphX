"""
Data visualization components for YouTube statistics
Creates interactive charts using matplotlib and plotly
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import numpy as np

from config import CHART_COLORS


class YouTubeCharts:
    """Class for creating YouTube statistics charts"""
    
    def __init__(self):
        """Initialize chart settings"""
        plt.style.use('dark_background')
        self.colors = CHART_COLORS
    
    def create_subscriber_chart(self, data: List[Dict], channel_name: str, 
                              use_plotly: bool = True) -> Optional[Figure]:
        """
        Create subscriber growth chart
        
        Args:
            data: List of subscriber data points
            channel_name: Name of the channel
            use_plotly: Whether to use plotly (True) or matplotlib (False)
            
        Returns:
            Chart figure
        """
        if not data:
            return None
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        if use_plotly:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['subscribers'],
                mode='lines+markers',
                name='Abonnenten',
                line=dict(color=self.colors['subscribers'], width=3),
                marker=dict(size=8, color=self.colors['subscribers']),
                fill='tonexty',
                fillcolor=f"rgba(255, 0, 0, 0.1)"
            ))
            
            fig.update_layout(
                title=f'Abonnentenentwicklung - {channel_name}',
                xaxis_title='Datum',
                yaxis_title='Abonnenten',
                plot_bgcolor=self.colors['background'],
                paper_bgcolor=self.colors['background'],
                font=dict(color='white'),
                xaxis=dict(
                    gridcolor=self.colors['grid'],
                    showgrid=True
                ),
                yaxis=dict(
                    gridcolor=self.colors['grid'],
                    showgrid=True,
                    tickformat=','
                ),
                hovermode='x unified'
            )
            
            return fig
        else:
            # Matplotlib version
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df['date'], df['subscribers'], 
                   color=self.colors['subscribers'], linewidth=3, marker='o', markersize=6)
            ax.fill_between(df['date'], df['subscribers'], alpha=0.3, 
                          color=self.colors['subscribers'])
            
            ax.set_title(f'Abonnentenentwicklung - {channel_name}', 
                        fontsize=16, color='white', fontweight='bold')
            ax.set_xlabel('Datum', color='white')
            ax.set_ylabel('Abonnenten', color='white')
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3, color=self.colors['grid'])
            
            # Format y-axis with commas
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            
            plt.tight_layout()
            return fig
    
    def create_view_chart(self, data: List[Dict], channel_name: str, 
                         use_plotly: bool = True) -> Optional[Figure]:
        """
        Create view count chart
        
        Args:
            data: List of view data points
            channel_name: Name of the channel
            use_plotly: Whether to use plotly (True) or matplotlib (False)
            
        Returns:
            Chart figure
        """
        if not data:
            return None
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        if use_plotly:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['views'],
                mode='lines+markers',
                name='Aufrufe',
                line=dict(color=self.colors['views'], width=3),
                marker=dict(size=8, color=self.colors['views']),
                fill='tonexty',
                fillcolor=f"rgba(0, 212, 170, 0.1)"
            ))
            
            fig.update_layout(
                title=f'Aufrufentwicklung - {channel_name}',
                xaxis_title='Datum',
                yaxis_title='Aufrufe',
                plot_bgcolor=self.colors['background'],
                paper_bgcolor=self.colors['background'],
                font=dict(color='white'),
                xaxis=dict(
                    gridcolor=self.colors['grid'],
                    showgrid=True
                ),
                yaxis=dict(
                    gridcolor=self.colors['grid'],
                    showgrid=True,
                    tickformat=','
                ),
                hovermode='x unified'
            )
            
            return fig
        else:
            # Matplotlib version
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df['date'], df['views'], 
                   color=self.colors['views'], linewidth=3, marker='o', markersize=6)
            ax.fill_between(df['date'], df['views'], alpha=0.3, 
                          color=self.colors['views'])
            
            ax.set_title(f'Aufrufentwicklung - {channel_name}', 
                        fontsize=16, color='white', fontweight='bold')
            ax.set_xlabel('Datum', color='white')
            ax.set_ylabel('Aufrufe', color='white')
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3, color=self.colors['grid'])
            
            # Format y-axis with commas
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            
            plt.tight_layout()
            return fig
    
    def create_video_chart(self, data: List[Dict], channel_name: str, 
                          use_plotly: bool = True) -> Optional[Figure]:
        """
        Create video count chart
        
        Args:
            data: List of video data points
            channel_name: Name of the channel
            use_plotly: Whether to use plotly (True) or matplotlib (False)
            
        Returns:
            Chart figure
        """
        if not data:
            return None
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        if use_plotly:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['videos'],
                mode='lines+markers',
                name='Videos',
                line=dict(color=self.colors['videos'], width=3),
                marker=dict(size=8, color=self.colors['videos']),
                fill='tonexty',
                fillcolor=f"rgba(255, 107, 53, 0.1)"
            ))
            
            fig.update_layout(
                title=f'Video-Entwicklung - {channel_name}',
                xaxis_title='Datum',
                yaxis_title='Videos',
                plot_bgcolor=self.colors['background'],
                paper_bgcolor=self.colors['background'],
                font=dict(color='white'),
                xaxis=dict(
                    gridcolor=self.colors['grid'],
                    showgrid=True
                ),
                yaxis=dict(
                    gridcolor=self.colors['grid'],
                    showgrid=True,
                    tickformat=','
                ),
                hovermode='x unified'
            )
            
            return fig
        else:
            # Matplotlib version
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df['date'], df['videos'], 
                   color=self.colors['videos'], linewidth=3, marker='o', markersize=6)
            ax.fill_between(df['date'], df['videos'], alpha=0.3, 
                          color=self.colors['videos'])
            
            ax.set_title(f'Video-Entwicklung - {channel_name}', 
                        fontsize=16, color='white', fontweight='bold')
            ax.set_xlabel('Datum', color='white')
            ax.set_ylabel('Videos', color='white')
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3, color=self.colors['grid'])
            
            # Format y-axis with commas
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            
            plt.tight_layout()
            return fig
    
    def create_combined_chart(self, subscriber_data: List[Dict], 
                            view_data: List[Dict], video_data: List[Dict], 
                            channel_name: str) -> Figure:
        """
        Create a combined chart with all three metrics
        
        Args:
            subscriber_data: Subscriber data points
            view_data: View data points
            video_data: Video data points
            channel_name: Name of the channel
            
        Returns:
            Combined chart figure
        """
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Abonnenten', 'Aufrufe', 'Videos'),
            vertical_spacing=0.1
        )
        
        # Subscriber chart
        if subscriber_data:
            df_subs = pd.DataFrame(subscriber_data)
            df_subs['date'] = pd.to_datetime(df_subs['date'])
            fig.add_trace(
                go.Scatter(x=df_subs['date'], y=df_subs['subscribers'], 
                          name='Abonnenten', line=dict(color=self.colors['subscribers'])),
                row=1, col=1
            )
        
        # View chart
        if view_data:
            df_views = pd.DataFrame(view_data)
            df_views['date'] = pd.to_datetime(df_views['date'])
            fig.add_trace(
                go.Scatter(x=df_views['date'], y=df_views['views'], 
                          name='Aufrufe', line=dict(color=self.colors['views'])),
                row=2, col=1
            )
        
        # Video chart
        if video_data:
            df_videos = pd.DataFrame(video_data)
            df_videos['date'] = pd.to_datetime(df_videos['date'])
            fig.add_trace(
                go.Scatter(x=df_videos['date'], y=df_videos['videos'], 
                          name='Videos', line=dict(color=self.colors['videos'])),
                row=3, col=1
            )
        
        fig.update_layout(
            title=f'Kanal-Entwicklung - {channel_name}',
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(color='white'),
            height=900,
            showlegend=False
        )
        
        # Update all subplots
        for i in range(1, 4):
            fig.update_xaxes(gridcolor=self.colors['grid'], showgrid=True, row=i, col=1)
            fig.update_yaxes(gridcolor=self.colors['grid'], showgrid=True, 
                           tickformat=',', row=i, col=1)
        
        return fig
    
    def create_stats_summary(self, channel_data: Dict) -> str:
        """
        Create a text summary of channel statistics
        
        Args:
            channel_data: Channel data dictionary
            
        Returns:
            Formatted statistics summary
        """
        def format_number(num: int) -> str:
            if num >= 1000000:
                return f"{num/1000000:.1f}M"
            elif num >= 1000:
                return f"{num/1000:.1f}K"
            return str(num)
        
        stats = f"""
📊 KANAL-STATISTIKEN
{'='*50}

📺 Kanal: {channel_data['title']}
🔗 URL: https://youtube.com/@{channel_data.get('custom_url', 'N/A')}

📈 Abonnenten: {format_number(channel_data['subscriber_count']):>10}
👀 Aufrufe:    {format_number(channel_data['view_count']):>10}
🎥 Videos:     {format_number(channel_data['video_count']):>10}

📅 Erstellt: {datetime.fromisoformat(channel_data['published_at'].replace('Z', '+00:00')).strftime('%d.%m.%Y')}

📝 Beschreibung:
{channel_data['description'][:200]}{'...' if len(channel_data['description']) > 200 else ''}
        """
        
        return stats.strip()


# Create global instance
youtube_charts = YouTubeCharts()
