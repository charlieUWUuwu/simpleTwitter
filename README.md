# simpleTwitter
- 提供用戶註冊、登入、訂閱、發文相關操作的超超簡易版推特
- 練習關聯式資料庫

## How to use
1. 啟動資料庫
```sh
docker compose up -d
```

2. 創建/啟動虛擬環境 `mariadb`，安裝後端所需套件
```sh
conda create --name mariadb python=3.10
conda activate mariadb
pip install -r ./backend/requirements.txt
```

3. (opt)初始化資料庫
```sh
cd simpleTwitter/backend
conda activate mariadb
python init_database.py
```

4. 啟動後端(接著可以用 postman 打)
```sh
cd simpleTwitter/backend
conda activate mariadb
python run.py
```

5. 結束後端
```sh
(ctrl+c)
```

6. 關閉資料庫(回到同一層資料夾)
```sh
docker compose down
```