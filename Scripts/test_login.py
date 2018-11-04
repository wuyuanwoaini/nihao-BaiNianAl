import sys,os
sys.path.append(os.getcwd())
import pytest
from Base.read_yaml import ReadYAML
import allure
from Page.page_in import PageIn

# 读取参数函数 封装
def get_data():
    # 自定义空列表
    arrs=[]
    # 获取出的结果为列表，列表内单个元素值为字典 datas.values()
    for data in ReadYAML("login_data.yaml").read_yaml().values():
        # 把读取出来的数据 组装成我需要的格式 [("","",""),("","","")]
        arrs.append((data.get("username"),data.get("password"),data.get("expect_result"),data.get("expect_toast")))
    # 返回组装后的结果
    return arrs

class TestLogin():
    # setup_class
    def setup_class(self):
        # 实例化 统一入口类
        self.page=PageIn()

        # 点击我
        self.login.page_click_me()
        # 点击 已有账号去登录
        self.login.page_click_name_ok_link()
    # teardown_class
    def teardown_class(self):
        # 关闭driver  驱动对象
        self.login.driver.quit()
    # test_login

    @pytest.mark.parametrize("username,password,expect_result",get_data())
    def test_login(self,username,password,expect_result):
        # 输入用户名
        self.login.page_input_username(username)
        # 输入密码
        self.login.page_input_pwd(password)
        # 点击登录
        self.login.page_click_login_btn()
        # 获取昵称
        nickname=self.login.page_get_nickname()
        try:
            assert expect_result in nickname
            # 设置
            self.login.page_click_setting()
            # 滑动 推送消息-》修改密码
            self.login.page_drag_and_drop()
            # 点击退出
            self.login.page_click_exit_btn()
            # 确认退出  注意：在此我们要关注，退出后的停留界面，因为循环遍历用例
            self.login.page_click_exit_btn_ok()
            # 下调用例的处理方式
            # 点击我
            self.login.page_click_me()
            # 点击 已有账号去登录
            self.login.page_click_name_ok_link()

        except:
            # 截图
            self.login.base_get_screenshot()
            # 失败图片写入报告
            with open ("./Image/faild.png","rb") as f:
                allure.attach("失败原因请查看附加图：",f.read(),allure.attach_type.PNG)
            # 抛异常
            raise
