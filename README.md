# The-RNG-game
---------------
##### 執行 theRNGgame.exe即可遊玩
##### 執行 seeyouritems.exe 即可看你的物品存檔
##### 更興(0.3後)把saves資料夾內的東西更換成就版本的，基本上都是互通的
##### .exe我放在[google drive](https://drive.google.com/drive/folders/1Hlspruu6U92JNcGjrff0HHDj5StzuZqH)上，以便下載原碼，不會被以為是病毒

# 更興注意事項
1. 將上版本的存檔丟到新版本內，***取代***新版本的原始存檔
2. 0.4以前轉後面的版本須將.rng改為.json

# 成就公式
1. **roll :**  $\frac {totalRoll}{1000} luck$
2. **time :**  $time(second) = 1800level + 60*level ^{\frac{1}{0.37}}$
# 備註
----------------
###### 如真想改的話直接從存檔改，如果你要真的完成就感的話，就別改了八，我懶得館

# updates
# v1.0.1 
**成就，沒了就這，做超久**
# v1.0.0 基本的抽取物品和儲存
#### 以下是v0.4以後更興概要
1. 興增了special item 和 extra item
    * special item 和 extra item 只能抽到一次
    * extra item 有特殊條件才能抽到
    * special item 和 extra item 皆有特殊動畫，抽到時會播放，也可以重播
2. 大改特改背包介面
    * 點下去後旁邊會有圖片
    * 有新的兩大分類!
    * 關閉按鈕
3. 興增了一大堆物品
    * 就不打出來了，以免據透
4. 抽東西時會有動畫了!
    * 詳情見 v0.4.4.10更新
5. 遊玩數據
    * 抽數和遊玩時間可以儲存了!
    * 有遊玩數據的介面了!
## v0.4.4.10
1. 興增抽取時的動畫
    + 會一直換圖片
    + 圖片以當下可以抽到的幸運加成再低一點
    + 圖片放置時會下降，下降越來越慢，公式為:
    $
    -1.5^{(-\frac{經過時間}{總撥放下降時間})} * {開始下降的最高點}
    $
    + 前後兩張圖片不回重複
2. 抽完動畫結束才撥放物品動畫
3. debug
    + 當該物品不再背包中且數量為0，無法抽取該extraItem

## v0.4.4.3
1. 興增了第一個extra item ，先不說名子，說了就爆露了
2. 微調介面
3. 興增了extra item 分類下有東西ㄌ
4. debug
    + 播放動畫時，無法強制退出，會轉圈圈
    + 撥放動畫時，強制alt + f4等退出放式，無法進行存檔
    + 現在撥放動畫時，可以強制退出遊戲 alt + f4 退出也會存檔，其他的我不確定，但只要時能測到的都可以正常退出並儲存
* 準備好1.0.0.0大更新，脫離beta版了 ( YA
## v0.4.3.1
1. 興增states 介面
2. 儲存抽取次數及遊玩時間
### v0.4.2.5
1. 更改物品欄介面
2. 點選物品後旁便會顯示圖示
3. special抽到後可以重播動畫
## v0.4.2 Special Item Update
1. debug
    * 解決當存檔空白無法抽的問題
    * 可重複抽special item
2. 啟用special item
3. 興增 1K 和 2025HappyNewYear
4. 興增動畫
5. 播放動畫完重新計時
### v0.4.1.11
1. 修正錯字
2. 更改讀取方式
3. 興增special item 和 extra item(有形態但尚未啟用)
4. 在背包有進行場景的切換
5. 在背包有 special item 和 extra item的分類
6. 更改背包滾動速度 (50 -> 75)
7. 更改背包介面
    * 將normal item往下放
    * 興增3個按鈕
+ 此版本沒有更興.exe
### v0.4.1.3
1. 興增場景，背包開啟時主畫面物品將不會顯示
2. 略改介面，興增關閉物品欄介面按鈕，開啟物品欄按鈕將無法關閉
3. 將按鈕全部設為只有左鍵能點擊
4. 自動存檔
### v0.4.0.6
* debug
## v0.4.0.5(物品欄更新)
1. 興增物品欄
2. 興增了4個物品
    * rare
    * veryRare
    * Epic
    * Line
3. 修改附檔名(.rng -> .json)

### v0.3.5.5
1. 去除無法儲存的bug，為補償之前的活動抽到無法存，下個版本(有special item時)將會重新開放抽取限定物品
2. 更換背景圖片
3. 2025 New Year Event 結束
4. 刪除之前所有物品可以抽到的
5. 重新興曾 common 、 uncommon、rock
6. 所有物品改成圖片
###### 備註: 此版本未匯出.exe

### v0.3.1  2025 New Year Event
1. remake quit button
2. add background
3. x3 luck event

## v0.3
#### 可以自動抽了
#### 放棄加密文件，改用正常的(反正有心要改的還是可以改)
#### 興曾抽的時間限制以及倒計時系統
#### 改寫部分函式
#### 重新匯出.exe