# Telegram机器人-千雪酱(KawaiChiyuki_bot)
## 机器人功能
> `{}`中的内容表示必填参数，`[]`中的参数表示选填参数，`|`分隔表示括号中的参数选一个即可
### Pixiv
- `/{day|week|month}_rank [page]` 获取`Pixiv{日|周|月}榜`的图片
- `/{day|week}_rank_r18 [page]` 获取`Pixiv R18{日|周}榜`的图片
- `/rank_g18g [page]` 获取`Pixiv R18G排行榜`的图片
> 在上述代码后加上页数可以获取更多图片,一页5张，共6页。不加默认获取排行榜前五张  
> 例：`/day_rank 2`  
> 获取Pixiv日榜第6-10张图片  
> 若页数为负数则是倒序发送
- `/sese` 随机获取Pixiv的图片
### 一言
- `/yan` 一言二次元语录
### Bangumi
- `/bangumi [weekday]` 获取当日更新的番剧，可选参数`weekday`的范围为`1-7`，代表周一到周日
> 例：`/bangumi 1` 获取周一更新的番剧

## 关于
一时兴起写的tg机器人，Python也是约等于没学过，边学边写，有不足的地方还请多多包涵

## 更新日志
### 2022.10.29
- 添加专门的函数输出发送/接收信息的日志，并完善了日志信息
- 整理了一下代码结构 ~~（以后有时间会再好好整理）~~
- 完善了代码中的注释

### 2022.10.26
- 添加了番剧日历的功能
- 完善了一些函数的日志输出
- 修改了对于机器人功能的表述

### 2022.10.22
- 修改了日志输出格式
- 添加了一言功能

### 2022.10.21
- 实现了随机获取Pixiv图片
- 完善了控制台输出的日志信息，在发送图片失败时会发送错误信息

### 2022.10.20
- 能发送的Pixiv图片不再限于前五张了,在命令后跟上页数以获取更多图片

### 2022.10.19
- 能够获取的Pixiv排行榜更多了
- 在发送图片失败时会发送错误信息

### 2022.10.18
- 能够获取Pixiv日榜及R18周榜的图片了

## TODO
- [x] 在发送了五张图片后再次发送指令能发送下五张图  
- [x] 使用`/sese`发送一张Pixiv随机图片
- [x] 获取新番时间表  
- [ ] 保存输出的日志
- [ ] 优化发送Pixiv排行榜图片的形式，避免刷屏
- [ ] 多线程优化
- [ ] 拦截同一用户短时间内的多次请求
- [ ] 模块化机器人功能，除基本功能外其余功能以插件形式加载

## 第三方API
- [HibiAPI](https://api.obfs.dev/docs)
- [一言](https://hitokoto.cn/)
- [Bangumi API](https://bangumi.github.io/api/#/)