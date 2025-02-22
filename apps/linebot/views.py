from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden

from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import \
        MessageEvent, TextSendMessage, \
        TextMessage, ImageMessage, VideoMessage, AudioMessage, FileMessage, \
        StickerMessage, LocationMessage, ImageSendMessage, VideoSendMessage, \
        AudioSendMessage, StickerSendMessage, LocationSendMessage, \
        FlexSendMessage, TemplateSendMessage, ButtonsTemplate, ConfirmTemplate, \
        CarouselTemplate, ImageCarouselTemplate
from linebot.webhook import SignatureValidator
from django.views.decorators.csrf import csrf_exempt

# 讀取環境變數
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        # 更安全的獲取簽名方式
        signature = request.headers.get('X-Line-Signature', '')
        if not signature:
            # print("無法獲取簽名")
            return HttpResponseForbidden("無法獲取簽名")
            
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
            
            if not events:
                # print("沒有事件需要處理")
                return HttpResponse("沒有事件需要處理")
                
            for event in events:
                if isinstance(event, MessageEvent):
                    mtext = event.message.text # 使用者傳來的訊息
                    message = []

                    if mtext == '文字':
                        message.append(
                            TextSendMessage(text=mtext)
                        )
                    elif mtext == '貼圖':
                        message.append(
                            StickerSendMessage(
                                package_id='1',
                                sticker_id='1'
                            )
                        )

                    # 最後回覆訊息
                    line_bot_api.reply_message(
                        event.reply_token,  # 針對回覆訊息的 token
                        message # 回覆訊息
                    )
                
            return HttpResponse("OK")
        except InvalidSignatureError as e:
            # print(f"簽名驗證失敗: {e}")
            return HttpResponseForbidden(f"簽名驗證失敗: {e}")
        except LineBotApiError as e:
            # print(f"LINE API 錯誤: {e}")
            return HttpResponseBadRequest(f"LINE API 錯誤: {e}")
        except Exception as e:
            # print(f"未預期的錯誤: {e}")
            return HttpResponseBadRequest(f"未預期的錯誤: {e}")
    else:
        return HttpResponse("這是 LINE Bot webhook")