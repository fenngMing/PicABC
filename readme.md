##  PicABC
一个极简但实用的开源图床

### 特性
- 支持带鉴权的图像上传和存储
- 支持从网络上拉取图片
- 支持使用本地客户端[PicGo](https://github.com/staugur/picbed)上传到自定义的PicABC图床

###  安装
- pip install -r requirements.txt

### 配置
 - **IMG_DIR**: local dir for storaging you  images
 - **TOKEN**: your password for upload new images

### 运行
 - python app.py

### [PicGo](https://github.com/staugur/picbed)客户端上传
- 安装node.js和PicGo
- 在PicGO中搜索并按照web-uploader 插件
- 在自定义web图床插件设置中如下配置：


```
API地址： www.你的域名/子域名.com/upload
Post参数名: img_data
Json路径: url
自定义Body: {"token":"你的个人Token"
```

### 其他
默认监听的是7777端口而非http 80端口，你可能需要增加一个Ngnix转发配置：
```
server {
    listen       80;
    charset utf-8;
    client_max_body_size 20M;
        root   /To/Your/Code;
        server_name 你的域名;

        location / {
       proxy_pass http://127.0.0.1:7777;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```

### 特别感谢
- [picbed](https://github.com/staugur/picbed) 给了我实现的参考
- [PicGo](https://github.com/staugur/picbed) 为我们提供了非常好的图床客户端程序
