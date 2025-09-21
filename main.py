"""
Command Line Interface for YouTube Statistics Tracker
Provides a simple CLI for analyzing YouTube channel data
"""

import argparse
import sys
from datetime import datetime
import matplotlib.pyplot as plt

from youtube_api import youtube_api
from charts import youtube_charts


def format_number(num: int) -> str:
    """Format large numbers with K/M suffixes"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)


def format_date(date_str: str) -> str:
    """Format date string for display"""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date.strftime('%d.%m.%Y')
    except:
        return date_str


def print_channel_info(channel_data):
    """Print formatted channel information"""
    print("\n" + "="*60)
    print(f"📺 KANAL: {channel_data['title']}")
    print("="*60)
    
    if channel_data.get('custom_url'):
        print(f"🔗 URL: https://youtube.com/@{channel_data['custom_url']}")
    
    print(f"📅 Erstellt: {format_date(channel_data['published_at'])}")
    print(f"📈 Abonnenten: {format_number(channel_data['subscriber_count']):>10}")
    print(f"👀 Aufrufe:    {format_number(channel_data['view_count']):>10}")
    print(f"🎥 Videos:     {format_number(channel_data['video_count']):>10}")
    
    avg_views = channel_data['view_count'] // max(channel_data['video_count'], 1)
    print(f"📊 Ø Aufrufe/Video: {format_number(avg_views):>10}")
    
    print("\n📝 Beschreibung:")
    description = channel_data['description']
    if len(description) > 200:
        description = description[:200] + "..."
    print(f"   {description}")
    print("="*60)


def print_recent_videos(videos, limit=5):
    """Print recent videos information"""
    if not videos:
        print("\n❌ Keine Videos gefunden.")
        return
    
    print(f"\n🎬 NEUESTE {min(limit, len(videos))} VIDEOS:")
    print("-" * 60)
    
    for i, video in enumerate(videos[:limit]):
        print(f"\n{i+1}. {video['title']}")
        print(f"   📅 {format_date(video['published_at'])}")
        print(f"   👀 {format_number(video['view_count'])} Aufrufe")
        print(f"   👍 {format_number(video['like_count'])} Likes")
        print(f"   💬 {format_number(video['comment_count'])} Kommentare")


def save_charts(channel_data, subscriber_history, view_history, video_history, output_dir="charts"):
    """Save charts as image files"""
    import os
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    channel_name = channel_data['title'].replace(' ', '_').replace('/', '_')
    
    print(f"\n💾 Speichere Diagramme in '{output_dir}/'...")
    
    # Subscriber chart
    sub_fig = youtube_charts.create_subscriber_chart(subscriber_history, channel_data['title'], use_plotly=False)
    if sub_fig:
        sub_fig.savefig(f"{output_dir}/{channel_name}_abonnenten.png", dpi=300, bbox_inches='tight')
        print(f"   ✅ Abonnenten-Diagramm gespeichert")
    
    # View chart
    view_fig = youtube_charts.create_view_chart(view_history, channel_data['title'], use_plotly=False)
    if view_fig:
        view_fig.savefig(f"{output_dir}/{channel_name}_aufrufe.png", dpi=300, bbox_inches='tight')
        print(f"   ✅ Aufruf-Diagramm gespeichert")
    
    # Video chart
    video_fig = youtube_charts.create_video_chart(video_history, channel_data['title'], use_plotly=False)
    if video_fig:
        video_fig.savefig(f"{output_dir}/{channel_name}_videos.png", dpi=300, bbox_inches='tight')
        print(f"   ✅ Video-Diagramm gespeichert")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="YouTube Statistics Tracker - Analysiere Kanal-Daten mit Diagrammen",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python main.py @google
  python main.py UC_x5XG1OV2P6uZZ5FSM9Ttw
  python main.py @pewdiepie --save-charts
  python main.py @MrBeast --videos 10 --output-dir my_charts
        """
    )
    
    parser.add_argument(
        'channel',
        help='YouTube-Kanal-ID oder Benutzername (z.B. @google oder UC_x5XG1OV2P6uZZ5FSM9Ttw)'
    )
    
    parser.add_argument(
        '--videos', '-v',
        type=int,
        default=5,
        help='Anzahl der neuesten Videos anzeigen (Standard: 5)'
    )
    
    parser.add_argument(
        '--save-charts', '-s',
        action='store_true',
        help='Diagramme als PNG-Dateien speichern'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='charts',
        help='Ausgabe-Verzeichnis für Diagramme (Standard: charts)'
    )
    
    parser.add_argument(
        '--no-videos',
        action='store_true',
        help='Keine Video-Informationen anzeigen'
    )
    
    args = parser.parse_args()
    
    print("🚀 YTGraphX - YouTube Statistics Tracker")
    print("=" * 50)
    
    try:
        print(f"🔍 Lade Daten für Kanal: {args.channel}")
        
        # Get comprehensive channel statistics
        stats = youtube_api.get_comprehensive_stats(args.channel)
        channel_data = stats['channel']
        videos = stats['videos']
        subscriber_history = stats['subscriber_history']
        view_history = stats['view_history']
        video_history = stats['video_history']
        
        # Print channel information
        print_channel_info(channel_data)
        
        # Print recent videos
        if not args.no_videos:
            print_recent_videos(videos, args.videos)
        
        # Save charts if requested
        if args.save_charts:
            save_charts(channel_data, subscriber_history, view_history, video_history, args.output_dir)
        
        # Print summary
        print(f"\n✅ Analyse abgeschlossen!")
        print(f"   📊 {len(subscriber_history)} Datenpunkte für Abonnenten-Entwicklung")
        print(f"   📊 {len(view_history)} Datenpunkte für Aufruf-Entwicklung")
        print(f"   📊 {len(video_history)} Datenpunkte für Video-Entwicklung")
        
        if args.save_charts:
            print(f"   💾 Diagramme gespeichert in: {args.output_dir}/")
        
    except KeyboardInterrupt:
        print("\n\n❌ Abgebrochen durch Benutzer.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fehler: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
