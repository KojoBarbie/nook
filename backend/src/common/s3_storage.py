"""S3でのデータ操作ユーティリティ。"""

import os
from datetime import datetime
from typing import List, Optional
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

class S3Storage:
    """
    S3でのデータ操作を担当するクラス。
    """
    
    def __init__(self):
        """
        S3Storageを初期化します。
        
        環境変数から以下の値を読み込みます：
        - AWS_ACCESS_KEY_ID: AWSのアクセスキー
        - AWS_SECRET_ACCESS_KEY: AWSのシークレットキー
        - AWS_BUCKET_NAME: S3バケット名
        """
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        if not self.bucket_name:
            raise ValueError("環境変数 'AWS_BUCKET_NAME' が設定されていません。")
    
    def _get_object_key(self, service_name: str, date: datetime) -> str:
        """
        オブジェクトキーを生成します。
        
        Parameters
        ----------
        service_name : str
            サービス名（ディレクトリ名）。
        date : datetime
            日付。
            
        Returns
        -------
        str
            オブジェクトキー。
        """
        date_str = date.strftime("%Y-%m-%d")
        return f"nook/{service_name}/{date_str}.md"
    
    def save_markdown(self, content: str, service_name: str, date: Optional[datetime] = None) -> str:
        """
        Markdownコンテンツを保存します。
        
        Parameters
        ----------
        content : str
            保存するMarkdownコンテンツ。
        service_name : str
            サービス名（ディレクトリ名）。
        date : datetime, optional
            日付。指定しない場合は現在の日付。
            
        Returns
        -------
        str
            保存されたオブジェクトのキー。
        """
        if date is None:
            date = datetime.now()
        
        object_key = self._get_object_key(service_name, date)
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=content.encode('utf-8'),
                ContentType='text/markdown'
            )
            return object_key
        except ClientError as e:
            raise Exception(f"S3への保存に失敗しました: {str(e)}")
    
    def load_markdown(self, service_name: str, date: Optional[datetime] = None) -> Optional[str]:
        """
        Markdownコンテンツを読み込みます。
        
        Parameters
        ----------
        service_name : str
            サービス名（ディレクトリ名）。
        date : datetime, optional
            日付。指定しない場合は現在の日付。
            
        Returns
        -------
        str or None
            読み込まれたMarkdownコンテンツ。ファイルが存在しない場合はNone。
        """
        if date is None:
            date = datetime.now()
        
        object_key = self._get_object_key(service_name, date)
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            raise Exception(f"S3からの読み込みに失敗しました: {str(e)}")
    
    def list_dates(self, service_name: str) -> List[datetime]:
        """
        利用可能な日付の一覧を取得します。
        
        Parameters
        ----------
        service_name : str
            サービス名（ディレクトリ名）。
            
        Returns
        -------
        List[datetime]
            利用可能な日付のリスト。
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"nook/{service_name}/"
            )
            
            dates = []
            for obj in response.get('Contents', []):
                key = obj['Key']
                if not key.endswith('.md'):
                    continue
                
                try:
                    date_str = key.split('/')[-1].replace('.md', '')
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    dates.append(date)
                except ValueError:
                    continue
            
            return sorted(dates, reverse=True)
        except ClientError as e:
            raise Exception(f"S3からのオブジェクト一覧取得に失敗しました: {str(e)}") 