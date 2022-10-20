# Telegram机器人-千雪酱(KawaiChiyuki_bot)

## 更新日志
### 2022.10.20
- 能发送的Pixiv图片不再限于前五张了,在命令后跟上页数以获取更多图片

### 2022.10.19
- 能够获取的Pixiv排行榜更多了
- 在发送图片失败时会发送错误信息

### 2022.10.18
- 能够获取Pixiv日榜及R18周榜的图片了

## 机器人功能
### Pixiv
- `/[day|week|month]_rank` 获取`Pixiv[日|周|月]榜`的图片
- `/[day|week]_rank_r18` 获取`Pixiv R18[日|周]榜`的图片
- `/rank_g18g` 获取`Pixiv R18G排行榜`的图片
> 在上述代码后加上页数可以获取更多图片,一页5张，共6页。不加默认获取排行榜前五张  
> 例：`/day_rank 2`  
> 获取Pixiv日榜第6-10张图片  
> 若页数为负数则是倒序发送

## 关于
一时兴起写的tg机器人，Python也是约等于没学过，边学边写，有不足的地方还请多多包涵

## TODO
-[x] 在发送了五张图片后再次发送指令能发送下五张图
-[ ] 使用`/sese`发送一张Pixiv随机图片
-[ ] 发图以外的别的功能(还没想好)

## 第三方API
- [HibiAPI](https://api.obfs.dev/docs)