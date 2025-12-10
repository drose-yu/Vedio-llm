# 生成AI视频
import dashscope
import requests
from dashscope import VideoSynthesis
import os



api_key = os.getenv('DASHCOPE_API_KEY') #填写你的百练api_key

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'


def create_vedio_by_qw():
    #发起请求
    request = VideoSynthesis.async_call( #异步发起请求
        model = 'wan2.5-t2v-preview',
        prompt="""
        一幅史诗级可爱的场景:
        一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。
        他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。
        悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。
        这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。
        整体氛围是“可爱”与“霸气”的搞笑和史诗般的融合。
        """,
        size = '480*832',
        watermark = False,
        seed = 44444, #随机种子
        prompt_extend = True,
        duration = 5,
        audio_url='https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3',
        # audio = True
    )
    print(type(request))
    # print("request:",request)
    if request.status_code == 200:
        request_id = request.request_id
        task_id = request.output.task_id
        task_status = request.output.task_status
        print("request_id:",request_id)
        print("task_id:",task_id)
        print("task_status:",task_status)

    try:
        response = VideoSynthesis.wait(request) #续查询任务，直到得到最终状态
        print(type(response))
        print("response:",response)
        if response.status_code == 200 and response.output.task_status == 'SUCCEEDED':
            video_url = response.output.video_url
            if video_url:
                #存储视频
                download_video_by_qw(video_url,f'vedio/{request.output.task_id}.mp4')

    except Exception as e:
        print('发生错误：',e)

def download_video_by_qw(video_url,save_path):
    try:
        resp = requests.get(video_url, stream=True, timeout=30)
        with open(save_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            print(f"视频下载成功,路径为{save_path}")
    except Exception as e:
        print(f"视频下载失败,原因：{e}")

if __name__ == '__main__':
    create_vedio_by_qw()
