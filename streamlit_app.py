"""
Streamlit Web Application for YouTube Statistics Tracker
Provides an interactive web interface for analyzing YouTube channel data
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

from youtube_api import youtube_api
from charts import youtube_charts
from config import CHART_COLORS


def format_number(num: int) -> str:
    """Format large numbers with K/M suffixes"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)


def format_date(date_input) -> str:
    """Format date string or datetime for display"""
    try:
        if isinstance(date_input, str):
            # Handle string input
            if 'T' in date_input:
                date = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
            else:
                date = datetime.fromisoformat(date_input)
        else:
            # Handle pandas datetime or other datetime objects
            date = pd.to_datetime(date_input)
        
        return date.strftime('%d.%m.%Y')
    except Exception as e:
        print(f"Date formatting error: {e}")
        return str(date_input)


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="YTGraphX - YouTube Statistics Tracker",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF0000, #CC0000);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 3rem;
    }
    .main-header p {
        color: #FFCCCC;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    .stats-card {
        background: #272727;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF0000;
        margin: 1rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #FF0000;
    }
    .metric-label {
        color: #CCCCCC;
        font-size: 1rem;
    }
    
    /* Fix text overlap and layout issues */
    .stContainer {
        margin-bottom: 1rem;
    }
    
    .video-container {
        margin-bottom: 2rem;
        padding: 1rem;
        border: 1px solid #333;
        border-radius: 8px;
        background: #1a1a1a;
    }
    
    .video-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        line-height: 1.4;
        word-wrap: break-word;
    }
    
    .video-stats {
        display: flex;
        gap: 1rem;
        margin-top: 0.5rem;
    }
    
    .video-stat {
        background: #333;
        padding: 0.5rem;
        border-radius: 4px;
        text-align: center;
        min-width: 80px;
    }
    
    /* Ensure proper spacing */
    .stMarkdown {
        margin-bottom: 0.5rem;
    }
    
    /* Fix caption styling */
    .stCaption {
        font-size: 0.9rem;
        color: #888;
        margin-top: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 YTGraphX</h1>
        <p>YouTube-Statistik-Tracker - Analysiere Kanal-Daten mit Diagrammen</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Kanal-Suche")
        
        # Search input
        channel_input = st.text_input(
            "YouTube-Kanal-ID oder Benutzername",
            placeholder="z.B. @google oder UC_x5XG1OV2P6uZZ5FSM9Ttw",
            help="Geben Sie eine YouTube-Kanal-ID oder einen Benutzernamen ein"
        )
        
        # Search button
        search_button = st.button("🔍 Kanal analysieren", type="primary", use_container_width=True)
        
        # Example channels
        st.markdown("### 📋 Beispiel-Kanäle")
        example_channels = {
            "Google": "@google",
            "PewDiePie": "@pewdiepie", 
            "MrBeast": "@MrBeast",
            "TED": "@TED"
        }
        
        for name, channel in example_channels.items():
            if st.button(f"📺 {name}", key=f"example_{name}"):
                channel_input = channel
                st.rerun()
    
    # Main content area
    if search_button and channel_input:
        with st.spinner("Lade Kanal-Daten..."):
            try:
                # Get channel data
                stats = youtube_api.get_comprehensive_stats(channel_input)
                channel_data = stats['channel']
                videos = stats['videos']
                
                # Store in session state
                st.session_state.channel_data = channel_data
                st.session_state.videos = videos
                st.session_state.subscriber_history = stats['subscriber_history']
                st.session_state.view_history = stats['view_history']
                st.session_state.video_history = stats['video_history']
                
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Fehler beim Laden der Kanal-Daten: {error_msg}")
                
                # Provide helpful suggestions
                if "quota" in error_msg.lower() or "403" in error_msg:
                    st.warning("💡 **API-Quota überschritten!** Warten Sie bis morgen oder überprüfen Sie Ihren API-Key.")
                elif "not found" in error_msg.lower() or "404" in error_msg:
                    st.info("💡 **Kanal nicht gefunden!** Versuchen Sie:")
                    st.write("- Eine andere Kanal-ID oder Benutzername")
                    st.write("- Ohne @-Symbol (z.B. 'google' statt '@google')")
                    st.write("- Eine vollständige Kanal-ID (z.B. 'UC_x5XG1OV2P6uZZ5FSM9Ttw')")
                elif "api key" in error_msg.lower():
                    st.warning("💡 **API-Key Problem!** Überprüfen Sie die Konfiguration in config.py")
                else:
                    st.info("💡 **Tipp:** Versuchen Sie einen anderen Kanal oder überprüfen Sie Ihre Internetverbindung.")
                
                st.stop()
    
    # Display channel data if available
    if 'channel_data' in st.session_state:
        channel_data = st.session_state.channel_data
        
        # Channel header
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.image(
                channel_data['thumbnails']['high']['url'],
                width=200
            )
        
        with col2:
            st.markdown(f"### {channel_data['title']}")
            if channel_data.get('custom_url'):
                st.markdown(f"**@**{channel_data['custom_url']}")
            
            st.markdown(f"**Erstellt:** {format_date(channel_data['published_at'])}")
            
            # Description
            description = channel_data['description']
            if len(description) > 300:
                description = description[:300] + "..."
            st.markdown(f"**Beschreibung:** {description}")
        
        # Statistics cards
        st.markdown("### 📊 Kanal-Statistiken")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="metric-value">{format_number(channel_data['subscriber_count'])}</div>
                <div class="metric-label">Abonnenten</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="metric-value">{format_number(channel_data['view_count'])}</div>
                <div class="metric-label">Aufrufe</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <div class="metric-value">{format_number(channel_data['video_count'])}</div>
                <div class="metric-label">Videos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_views = channel_data['view_count'] // max(channel_data['video_count'], 1)
            st.markdown(f"""
            <div class="stats-card">
                <div class="metric-value">{format_number(avg_views)}</div>
                <div class="metric-label">Ø Aufrufe/Video</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts section
        st.markdown("### 📈 Kanal-Entwicklung")
        
        # Chart tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Alle Diagramme", "👥 Abonnenten", "👀 Aufrufe", "🎥 Videos"])
        
        with tab1:
            # Combined chart
            combined_fig = youtube_charts.create_combined_chart(
                st.session_state.subscriber_history,
                st.session_state.view_history,
                st.session_state.video_history,
                channel_data['title']
            )
            st.plotly_chart(combined_fig, use_container_width=True)
        
        with tab2:
            # Subscriber chart
            sub_fig = youtube_charts.create_subscriber_chart(
                st.session_state.subscriber_history,
                channel_data['title']
            )
            if sub_fig:
                st.plotly_chart(sub_fig, use_container_width=True)
        
        with tab3:
            # View chart
            view_fig = youtube_charts.create_view_chart(
                st.session_state.view_history,
                channel_data['title']
            )
            if view_fig:
                st.plotly_chart(view_fig, use_container_width=True)
        
        with tab4:
            # Video chart
            video_fig = youtube_charts.create_video_chart(
                st.session_state.video_history,
                channel_data['title']
            )
            if video_fig:
                st.plotly_chart(video_fig, use_container_width=True)
        
        # Recent videos section
        st.markdown("### 🎬 Neueste Videos")
        
        if st.session_state.videos:
            # Create videos dataframe
            videos_df = pd.DataFrame(st.session_state.videos)
            videos_df['published_at'] = pd.to_datetime(videos_df['published_at'])
            videos_df = videos_df.sort_values('published_at', ascending=False)
            
            # Display videos in a cleaner format
            for i, video in enumerate(videos_df.head(6).iterrows()):
                video_data = video[1]
                
                # Create a container for each video with custom styling
                st.markdown(f"""
                <div class="video-container">
                    <div class="video-title">{i+1}. {video_data['title'][:100]}{'...' if len(video_data['title']) > 100 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.image(
                        video_data['thumbnails']['medium']['url'],
                        width=200
                    )
                
                with col2:
                    # Video stats in a clean format using metrics
                    col_stats1, col_stats2, col_stats3 = st.columns(3)
                    
                    with col_stats1:
                        st.metric("👀 Aufrufe", format_number(video_data['view_count']))
                    
                    with col_stats2:
                        st.metric("👍 Likes", format_number(video_data['like_count']))
                    
                    with col_stats3:
                        st.metric("💬 Kommentare", format_number(video_data['comment_count']))
                    
                    # Date
                    st.caption(f"📅 {format_date(video_data['published_at'])}")
                
                st.divider()
        else:
            st.info("Keine Videos gefunden.")
        
        # Data export
        st.markdown("### 💾 Daten exportieren")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Statistiken als CSV exportieren"):
                # Create summary data
                summary_data = {
                    'Metrik': ['Abonnenten', 'Aufrufe', 'Videos', 'Durchschnittliche Aufrufe pro Video'],
                    'Wert': [
                        channel_data['subscriber_count'],
                        channel_data['view_count'],
                        channel_data['video_count'],
                        channel_data['view_count'] // max(channel_data['video_count'], 1)
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 CSV herunterladen",
                    data=csv,
                    file_name=f"{channel_data['title']}_statistiken.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Historische Daten als CSV exportieren"):
                # Combine all historical data
                historical_data = {
                    'Datum': [point['date'] for point in st.session_state.subscriber_history],
                    'Abonnenten': [point['subscribers'] for point in st.session_state.subscriber_history],
                    'Aufrufe': [point['views'] for point in st.session_state.view_history],
                    'Videos': [point['videos'] for point in st.session_state.video_history]
                }
                historical_df = pd.DataFrame(historical_data)
                csv = historical_df.to_csv(index=False)
                st.download_button(
                    label="📥 CSV herunterladen",
                    data=csv,
                    file_name=f"{channel_data['title']}_historische_daten.csv",
                    mime="text/csv"
                )
    
    else:
        # Welcome screen
        st.markdown("""
        ## 🎯 Willkommen bei YTGraphX!
        
        **YTGraphX** ist ein leistungsstarker YouTube-Statistik-Tracker, der Ihnen hilft, 
        detaillierte Einblicke in YouTube-Kanäle zu gewinnen.
        
        ### ✨ Features:
        - 📊 **Interaktive Diagramme** für Abonnenten-, Aufruf- und Video-Entwicklung
        - 🔍 **Einfache Kanal-Suche** per ID oder Benutzername
        - 📈 **Trend-Analyse** mit historischen Daten
        - 💾 **Daten-Export** in verschiedenen Formaten
        - 📱 **Responsive Design** für alle Geräte
        
        ### 🚀 So starten Sie:
        1. Geben Sie eine YouTube-Kanal-ID oder einen Benutzernamen in die Seitenleiste ein
        2. Klicken Sie auf "Kanal analysieren"
        3. Erkunden Sie die detaillierten Statistiken und Diagramme
        
        ### 💡 Tipp:
        Verwenden Sie die Beispiel-Kanäle in der Seitenleiste für einen schnellen Start!
        """)
        
        # Show example charts
        st.markdown("### 📊 Beispiel-Diagramme")
        
        # Create sample data for demonstration
        import numpy as np
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='ME')
        sample_data = {
            'subscribers': [1000 + i * 100 + np.random.randint(-50, 150) for i in range(len(dates))],
            'views': [10000 + i * 1000 + np.random.randint(-500, 1500) for i in range(len(dates))],
            'videos': [10 + i + np.random.randint(-2, 3) for i in range(len(dates))]
        }
        
        sample_subscriber_data = [{'date': d.strftime('%Y-%m-%d'), 'subscribers': s} for d, s in zip(dates, sample_data['subscribers'])]
        sample_view_data = [{'date': d.strftime('%Y-%m-%d'), 'views': v} for d, v in zip(dates, sample_data['views'])]
        sample_video_data = [{'date': d.strftime('%Y-%m-%d'), 'videos': v} for d, v in zip(dates, sample_data['videos'])]
        
        # Show sample charts
        sample_fig = youtube_charts.create_combined_chart(
            sample_subscriber_data,
            sample_view_data, 
            sample_video_data,
            "Beispiel-Kanal"
        )
        st.plotly_chart(sample_fig, use_container_width=True)


if __name__ == "__main__":
    main()
