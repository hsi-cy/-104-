from spider104 import spider104

def spider(keyword, area):
    """創建 jobs dataframe 抓資料"""
    start = timeit.default_timer()
    spider = spider104(keyword, area)
    spider.openBrowser()
    spider.scrollDown()
    spider.clickNextPage()
    List = spider.getAllLinks()
    print('共有'+ str(len(List)) + '筆資料')

    jobsDF = pd.DataFrame()

    for i in range(len(List)):
        link = List[i].attrs['href'].strip('//')
        spider.goToPage('https://' + link)
        sleep(0.35)
        try:
            jobsDF = spider.scrapeData(jobsDF)

            percentage = round((i+1)/len(List),2)
            if percentage == 0.25:
                print('目前進度至 25% 已抓取' + str(i+1) +'筆資料')
            elif percentage == 0.5:
                print('目前進度至 50% 已抓取' + str(i+1) +'筆資料')
            elif percentage == 0.75:
                print('目前進度至 75% 已抓取' + str(i+1) +'筆資料')
            elif percentage == 1:
                print('任務完成！ 已抓取' + str(i+1) +'筆資料')
        except:
            try:
                jobsDF = spider.scrapeData(jobsDF)

                percentage = round((i+1)/len(List),2)
                if percentage == 0.25:
                    print('目前進度至 25% 已抓取' + str(i+1) +'筆資料')
                elif percentage == 0.5:
                    print('目前進度至 50% 已抓取' + str(i+1) +'筆資料')
                elif percentage == 0.75:
                    print('目前進度至 75% 已抓取' + str(i+1) +'筆資料')
                elif percentage == 1:
                    print('任務完成！ 已抓取' + str(i+1) +'筆資料')
            
            except Exception as e:
                print(e)

    spider.closeBrowser()
    stop = timeit.default_timer()
    print('Time: ', stop - start) 

    return (jobsDF)