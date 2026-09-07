# 圖解庫

規格：原創剖面、白底、中英編號標註、藍／橙能量／物流箭嘴、教科書解剖圖風格。

**進度：149 / 149 編號項 + 咖啡機示範 1 張 = 150 張 JPG。完成率 100%。**

| 章 | 編號 | 狀態 |
|----|------|------|
| 第1章 機械的起源 | 001–004 | ✅ |
| 第2章 住家機械 | 005–037 + 咖啡機 | ✅ |
| 第3章 辦公與醫療機械 | 038–055 | ✅ |
| 第4章 戶外機械 | 056–073 | ✅ |
| 第5章 休閒娛樂機械 | 074–091 | ✅ |
| 第6章 運輸機械 | 092–123 | ✅（本批補 118–123） |
| 第7章 產業機械 | 124–141 | ✅（本批補 124–126、128、130–141；127／129 早已齊） |
| 第8章 夢想與未來機械 | 142–149 | ✅ |

本批新增 30 張：118–126、128、130–149。

JPG 共 150 張（合計約 51 MB）存在本機 `圖解/`。GitHub Contents API 不適合一次推 50 MB 二進制；請在自己部機用 Git LFS：

```bash
git clone git@github.com:yip-lgtm/mech-Eng-Bootcamp.git
# copy local 圖解/*.jpg into
# 24_Week_Weekend_Bootcamp/機械構造解剖圖鑑/圖解/
git lfs install
git lfs track "24_Week_Weekend_Bootcamp/機械構造解剖圖鑑/圖解/*.jpg"
git add .gitattributes 24_Week_Weekend_Bootcamp/機械構造解剖圖鑑/圖解
git commit -m "Add 149 cutaway diagrams (LFS)"
git push origin main
```
