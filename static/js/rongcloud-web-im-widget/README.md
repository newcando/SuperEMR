# RongCloud Web IM Widget for Angular

---

**Web IM Widget for Angular** 是一个angular插件。通信部分依赖 `RongIMLib`。  
支持IE9+、Chrome、Firefox等

```
npm install -g typescript@1.6.0beta tsd grunt-cli
```

如有必要，使用 `sudo npm`

### 安装依赖库

在项目根目录下执行：

```
npm install
tsd install
```

### 编译开发代码

```
grunt build
```

### 发布正式代码

```
grunt release
```

### 编译demo

```
grunt demo
```

### 启动demo服务

```
grunt connect:demo
```

## 文件结构说明
```
  |-----------------------
  |  demo实例
  |            [demo/user1]用户1
  |            [demo/user2]用户2
  |            [demo/widget]插件所需文件
  |            [demo/vendor]依赖资源
  |            [demo/index]
  |------------------------
  |  dist插件资源目录
  |				[dist/css]样式资源
  |				[dist/images]图片资源
  |				[dist/RongIMWidget.js] IM 插件
  |-----------------------
  |  doc文档说明
  |				[doc/开发文档]
  |				[doc/客服]关于客服使用的说明
  |-----------------------
  |  src源码
  |				[]
  |
  |-----------------------
  | vendor 依赖 js 插件库
  |
```
