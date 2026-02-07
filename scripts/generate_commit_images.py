#!/usr/bin/env python3
"""
Generate visual representations (images) of Git commit history for the Omnimathematics Penalty Framework.
"""

import os
import subprocess
import sys

# Try importing matplotlib and numpy, installing if needed
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime
    import numpy as np
    from collections import defaultdict
    import json
except ImportError as e:
    print(f"Required packages not found: {e}")
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "numpy"])
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import datetime
    import numpy as np
    from collections import defaultdict
    import json

def get_commit_data():
    """Extract commit data from the Git repository."""
    try:
        # Get commit hash, date, author, and message
        cmd = [
            "git", "log", 
            "--pretty=format:{\"hash\":\"%H\",\"date\":\"%ai\",\"author\":\"%an <%ae>\",\"message\":\"%s\"}",
            "--date=iso"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    commit_info = json.loads(line)
                    # Parse the ISO date string
                    commit_info['date'] = datetime.fromisoformat(commit_info['date'].replace(' ', 'T'))
                    commits.append(commit_info)
                except json.JSONDecodeError:
                    continue
        
        return commits
    except subprocess.CalledProcessError:
        print("Error: Not a Git repository or Git not installed.")
        return []

def plot_commit_timeline(commits, output_file="commit_timeline.png"):
    """Create a timeline visualization of commits."""
    if not commits:
        print("No commit data to visualize.")
        return
    
    dates = [c['date'] for c in commits]
    authors = [c['author'] for c in commits]
    
    # Count commits by author
    author_counts = defaultdict(int)
    for author in authors:
        author_counts[author] += 1
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Timeline plot
    ax1.scatter(dates, [1]*len(dates), alpha=0.6, s=50)
    ax1.set_title('Commit Timeline - Omnimathematics Penalty Framework', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Commits')
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Format x-axis to show dates nicely
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # Author contribution bar chart
    unique_authors = list(author_counts.keys())
    counts = list(author_counts.values())
    
    bars = ax2.bar(range(len(unique_authors)), counts, tick_label=unique_authors)
    ax2.set_title('Commit Contributions by Author', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Author')
    ax2.set_ylabel('Number of Commits')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")
    
    # Add count labels on top of bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Timeline visualization saved to {output_file}")

def plot_commit_activity_heatmap(commits, output_file="commit_activity_heatmap.png"):
    """Create a heatmap showing commit activity by day of week and hour."""
    if not commits:
        print("No commit data to visualize.")
        return
    
    # Extract day of week and hour from commit dates
    days_of_week = [c['date'].weekday() for c in commits]  # Monday is 0, Sunday is 6
    hours = [c['date'].hour for c in commits]
    
    # Create a 2D histogram
    heatmap, xedges, yedges = np.histogram2d(days_of_week, hours, bins=[7, 24], 
                                            range=[[0, 6], [0, 23]])
    
    # Create the heatmap
    fig, ax = plt.subplots(figsize=(16, 6))
    
    im = ax.imshow(heatmap, cmap='YlOrRd', aspect='auto', origin='lower')
    
    # Set ticks and labels
    ax.set_xticks(range(24))
    ax.set_xticklabels([f"{i}:00" for i in range(24)], rotation=45)
    ax.set_yticks(range(7))
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    
    ax.set_title('Commit Activity Heatmap - Omnimathematics Penalty Framework', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Day of Week')
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Number of Commits')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Heatmap visualization saved to {output_file}")

def plot_commit_evolution(commits, output_file="commit_evolution.png"):
    """Plot cumulative commits over time."""
    if not commits:
        print("No commit data to visualize.")
        return
    
    # Sort commits by date
    sorted_commits = sorted(commits, key=lambda x: x['date'])
    
    dates = [c['date'] for c in sorted_commits]
    cumulative_count = list(range(1, len(dates) + 1))
    
    plt.figure(figsize=(14, 6))
    plt.plot(dates, cumulative_count, marker='o', linewidth=2, markersize=4)
    plt.title('Cumulative Commit Growth - Omnimathematics Penalty Framework', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Number of Commits')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Cumulative commits visualization saved to {output_file}")

def main():
    """Generate all commit visualizations."""
    print("Generating commit images for Omnimathematics Penalty Framework...")
    
    # Change to the repository directory
    repo_dir = "/home/new/mttech/Omniscient_Lint/Folders/Gitshit/penalty"
    os.chdir(repo_dir)
    
    # Get commit data
    commits = get_commit_data()
    
    if not commits:
        print("Could not retrieve commit data. Please ensure you're in a Git repository.")
        return
    
    print(f"Found {len(commits)} commits to visualize.")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(repo_dir, "commit_images")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate visualizations
    plot_commit_timeline(commits, os.path.join(output_dir, "timeline.png"))
    plot_commit_activity_heatmap(commits, os.path.join(output_dir, "heatmap.png"))
    plot_commit_evolution(commits, os.path.join(output_dir, "evolution.png"))
    
    print(f"\nAll commit images have been saved to the '{output_dir}' directory.")
    print("\nGenerated images:")
    print("- timeline.png: Shows commit timeline and author contributions")
    print("- heatmap.png: Shows commit activity by day of week and hour")
    print("- evolution.png: Shows cumulative commit growth over time")

if __name__ == "__main__":
    main()