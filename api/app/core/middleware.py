from fastapi.middleware.cors import CORSMiddleware

# CORSミドルウェア
CORS = {
    "middleware_class": CORSMiddleware,
    "allow_origins": [
        # ローカルフロントAPP
        "http://localhost:3000",
    ],
    "allow_methods": ["*"],
    "allow_headers": ["*"],
    "expose_headers": [
        # 標準のファイル名
        "Content-Disposition",
        # ファイル名カスタムヘッダー
        "X-File-Name"
    ]
}