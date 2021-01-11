# Personalized-Evaluation-System
## 针对学生的个性化评价系统

### 系统描述：
（1）目的：根据学生的上课情况和学习状态，做出成绩预测以及针对每名学生个性化的评价。  
（2）主要功能：通过学习平台或者网络爬虫获取学生上课状态和课堂讨论数据，运用深度学习自然语言
处理技术，预测学生的成绩。构建心理学模型，对学生做出分类预测并做出个性化评价，实现因材施教。

### 数据来源：
- [北京大学moodle学习平台](http://120.77.86.170/moodle/)
- 社交平台

### 成果展示：
 - [网站](https://tesseract-r.github.io/Personalized-Evaluation-System/)

### 可行性研究报告：[链接](可研报告/可研报告.pdf)
### 需求规约说明书：[链接](https://github.com/Tesseract-R/Personalized-Evaluation-System/blob/main/%E9%9C%80%E6%B1%82%E5%88%86%E6%9E%90/%E9%9C%80%E6%B1%82%E8%A7%84%E6%A0%BC%E8%AF%B4%E6%98%8E%E4%B9%A6%20%2B%20%E7%AC%AC%E5%85%AB%E7%BB%84%20%2B%20%E9%92%88%E5%AF%B9%E5%AD%A6%E7%94%9F%E7%9A%84%E4%B8%AA%E6%80%A7%E5%8C%96%E8%AF%84%E4%BB%B7%E7%B3%BB%E7%BB%9F.pdf)
### 概要设计说明书：[链接](https://github.com/Tesseract-R/Personalized-Evaluation-System/blob/main/%E6%A6%82%E8%A6%81%E8%AE%BE%E8%AE%A1/%E6%A6%82%E8%A6%81%E8%AE%BE%E8%AE%A1%E8%AF%B4%E6%98%8E%E4%B9%A6%20%2B%20%E7%AC%AC%E5%85%AB%E7%BB%84%20%2B%20%E9%92%88%E5%AF%B9%E5%AD%A6%E7%94%9F%E7%9A%84%E4%B8%AA%E6%80%A7%E5%8C%96%E8%AF%84%E4%BB%B7%E7%B3%BB%E7%BB%9F.pdf)

### 详细设计说明书：[链接](https://github.com/Tesseract-R/Personalized-Evaluation-System/blob/main/%E8%AF%A6%E7%BB%86%E8%AE%BE%E8%AE%A1/%E8%AF%A6%E7%BB%86%E8%AE%BE%E8%AE%A1%E8%AF%B4%E6%98%8E%E4%B9%A6%20%2B%20%E7%AC%AC%E5%85%AB%E7%BB%84%20%2B%20%E9%92%88%E5%AF%B9%E5%AD%A6%E7%94%9F%E7%9A%84%E4%B8%AA%E6%80%A7%E5%8C%96%E8%AF%84%E4%BB%B7%E7%B3%BB%E7%BB%9F.pdf)

### 第一次线下会议记录（11/13）：[链接](https://github.com/Tesseract-R/Personalized-Evaluation-System/blob/main/%E4%BC%9A%E8%AE%AE%E8%AE%B0%E5%BD%95/11%E6%9C%8813%E6%97%A5%E4%BC%9A%E8%AE%AE%E8%AE%B0%E5%BD%95.md)

### 第二次线下会议记录（11/18）：[链接](https://github.com/Tesseract-R/Personalized-Evaluation-System/blob/main/%E4%BC%9A%E8%AE%AE%E8%AE%B0%E5%BD%95/11%E6%9C%8818%E6%97%A5%E4%BC%9A%E8%AE%AE%E8%AE%B0%E5%BD%95.md)

### 第三次线下会议记录（12/2）：[链接](https://github.com/Tesseract-R/Personalized-Evaluation-System/blob/main/%E4%BC%9A%E8%AE%AE%E8%AE%B0%E5%BD%95/12%E6%9C%882%E6%97%A5%E4%BC%9A%E8%AE%AE%E8%AE%B0%E5%BD%95.png)

```mermaid
gantt
dateFormat  YYYY-MM-DD
title 系统开发甘特图
section 设计
可行性研究	:done,    des1, 2020-10-18,2020-10-29
需求分析     :done,    des2, 2020-11-02,2020-11-12
概要设计     :done,    des3, 2020-11-17, 2020-11-25
详细设计     :done,    des4, 2020-11-30, 2020-12-08

section 编码
	成绩预测模块       :crit, done, 2020-12-02,2021-01-13
	个性化评价生成模块  :crit, done, 2020-12-02,2021-01-13
web框架           :crit, done, 2020-12-02,2021-01-13
模块集成           :crit, done, 2021-01-11,2021-01-15

section 测试
功能测试           :done,   a1, 2021-01-10, 3d
压力测试           :active， 2021-01-12, 3d
测试报告           :done,2021-01-12,1d
```
