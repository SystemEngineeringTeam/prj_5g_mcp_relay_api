# HTTPリクエストをWebSocketで中継するAPI

## セットアップ
```bash
pip install -r requirements.txt
```

## 起動
### 開発環境
```bash
uvicorn main:app --reload
```

### 本番環境
```bash
uvicorn main:app --host 0.0.0.0
```
