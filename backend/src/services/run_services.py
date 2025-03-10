"""
Nookの各サービスを実行するスクリプト。
情報を収集し、ローカルストレージに保存します。
"""

import os
import argparse
from datetime import datetime
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# GitHubトレンドサービス
from src.services.github_trending.github_trending import GitHubTrending

# 他のサービスをインポート
from src.services.hacker_news.hacker_news import HackerNewsRetriever
from src.services.reddit_explorer.reddit_explorer import RedditExplorer
from src.services.tech_feed.tech_feed import TechFeed
from src.services.paper_summarizer.paper_summarizer import PaperSummarizer

def run_github_trending():
    """
    GitHubトレンドサービスを実行します。
    """
    print("GitHubトレンドリポジトリを収集しています...")
    github_trending = GitHubTrending()
    github_trending.run()
    print("GitHubトレンドリポジトリの収集が完了しました。")

def run_hacker_news():
    """
    Hacker Newsサービスを実行します。
    """
    print("Hacker News記事を収集しています...")
    try:
        # クラス名を修正
        hacker_news = HackerNewsRetriever()
        hacker_news.run()
        print("Hacker News記事の収集が完了しました。")
    except Exception as e:
        print(f"Hacker News記事の収集中にエラーが発生しました: {str(e)}")

def run_reddit_explorer():
    """
    Redditエクスプローラーサービスを実行します。
    """
    print("Reddit投稿を収集しています...")
    try:
        # APIキーの確認
        if not os.environ.get("REDDIT_CLIENT_ID") or not os.environ.get("REDDIT_CLIENT_SECRET"):
            print("警告: REDDIT_CLIENT_ID または REDDIT_CLIENT_SECRET が設定されていません。")
            print("Reddit APIを使用するには、これらの環境変数を設定してください。")
            return
            
        reddit_explorer = RedditExplorer()
        reddit_explorer.run()
        print("Reddit投稿の収集が完了しました。")
    except Exception as e:
        print(f"Reddit投稿の収集中にエラーが発生しました: {str(e)}")

def run_tech_feed():
    """
    技術フィードサービスを実行します。
    """
    print("技術ブログのフィードを収集しています...")
    try:
        tech_feed = TechFeed()
        tech_feed.run()
        print("技術ブログのフィードの収集が完了しました。")
    except Exception as e:
        print(f"技術ブログのフィード収集中にエラーが発生しました: {str(e)}")

def run_paper_summarizer():
    """
    論文要約サービスを実行します。
    """
    print("arXiv論文を収集・要約しています...")
    try:
        # OpenAI APIキーの確認
        if not os.environ.get("OPENAI_API_KEY"):
            print("警告: OPENAI_API_KEY が設定されていません。")
            print("論文要約には OpenAI API が必要です。")
            return
            
        paper_summarizer = PaperSummarizer()
        paper_summarizer.run()
        print("論文の収集・要約が完了しました。")
    except Exception as e:
        print(f"論文の収集・要約中にエラーが発生しました: {str(e)}")

def main():
    """
    コマンドライン引数に基づいて、指定されたサービスを実行します。
    """
    parser = argparse.ArgumentParser(description="Nookサービスを実行します")
    parser.add_argument(
        "--service", 
        type=str,
            choices=["all", "github", "hackernews", "reddit", "techfeed", "paper"],
        default="all",
        help="実行するサービス (デフォルト: all)"
    )
    
    args = parser.parse_args()
    
    if args.service == "all" or args.service == "github":
        run_github_trending()
    
    if args.service == "all" or args.service == "hackernews":
        run_hacker_news()
    
    if args.service == "all" or args.service == "reddit":
        run_reddit_explorer()
    
    if args.service == "all" or args.service == "techfeed":
        run_tech_feed()
    
    if args.service == "all" or args.service == "paper":
        run_paper_summarizer()

if __name__ == "__main__":
    main() 