=====================================================================================================
		EMS JSON接口协议 v0.1
		By Raymond Wu
		On Aug 19, 2024
		
		CHG_1. Aug 19, 2024
			初版
		CHG_2. Aug 26, 2024
			调整接口定义
			删除了原8.1下8.1.1管理员查询可以连接系统列表和8.1.2对指定的系统, 管理员添加人员
		CHG_3. Aug 29, 2024
			修改错误			
		CHG_4. Sep 9, 2024
			修改了 1.2 超级管理员新建修改激活禁止系统
			请求验证码, 加返回OK, 
			约定:
				账号名称长度10个汉字
				空间名称长度10个汉字
				设备名称, 包括主机/节点/设备/传感器/执行器/计划程序/定制场景, 长度10个汉字
				单位名称/显示系统名称长度20个汉字
			
=====================================================================================================

JSON接口依据小程序和WEB操作过程进行设计。
1. 云端WEB地址: www.joiningtek.cn
2. 主机web地址:(默认) 192.168.1.65
3. 客户系统构成方案
3.1	主机服务器方案, 物联网设备(LoRaWAN节点)通过网关节点采用MQTT连接主机服务器, 主机服务器采用MQTT接入云端
3.2 免服务器方案(server-less), 物联网设备(LoRaWAN节点)经由网关节点采用MQTT接入云端
3.3 用户终端采用websocket方式接入云端, 云端对用户定义的信息进行主动推送
4. 用户界面
4.1 WEB界面
4.1.1 超级管理员界面, 用于在后台新建和管理系统, 仅限于系统名称/管理员/背景图
4.1.2 平台界面, 用户操作进入界面, 于网页的右上方
4.2 小程序
4.2.1 钉钉小程序, 用户操作界面
4.2.2 微信小程序, 用户操作界面

JSON接口分以下部分:
1. 超级管理员
2. 注册登录
3. 空间管理
4. 设备管理
5. 定制管理
6. 操作管理
7. 报告管理
8. 人员管理

数据交互:
1. 云端推送数据根据接口定义
2. 注册过程
2.1 注册名称查重
2.2 获取手机验证码
2.3 提交注册
2.4 所有的注册, 系统都会赋予唯一的ID, 不要显示在界面上
3. 交互规则
3.1 用户向系统提交请求时, 必须提交包括但不限于以下内容
	{
		"todo",			"TODO",							// 做什么
		"systemID",		"systemID",						// 哪一个系统
		"userID",		"userID",						// 你是谁
		"token",		"TOKEN",						// 验证你的身份
			
		"hostID",		"hostID",						// 相关的重要信息
		"devEUI",		"devEUI",						// 等等 
		......
		
		"needAnswer", 	"yes"							// 是否需要回复
	}
3.2 用户请求并且需要返回的
3.2.1 返回成功
3.2.1.1 有数据的, 根据定义的数据接口, 返回"code, 0, 'returnMsg'"
3.2.1.2 没有数据的, 返回"code， OK"
3.2.3 返回失败, 
3.2.2.1 "code， 1", 表示不能识别请求
3.2.2.2 "code， 2", 表示请求可以识别, 参数无效
3.2.2.3 "code， 3， errNo， 'errMsg'", 表示请求和参数有效, errMsg是具体陈述, 界面在显示
3.3 xxxID和xxxNo的区别
3.3.1 xxxID是系统赋予, 称为序号
3.3.2 xxxNo是用户设置, 称为编号


JSON接口索引
--------------------------------------------------------------------------------------
1. 超级管理员
1.1 超级管理员登录
1.1.1 获取短信验证码	GET_SUPERVERIFY 				L166
1.1.2 超级管理员登录	SET_SUPERLOGIN 					L174
1.2 超级管理员新建修改激活禁止系统 
1.2.1 系统和管理管账号查重	QRY_SYSNAME 			L198
1.2.2 获取短信验证码	GET_ADMINVERIFY 				L230
1.2.3 新建系统	ADD_NEWSYSTEM 						L239
1.2.4 修改系统	MDF_CURSYSTEM 						L272
1.2.5 上传网页背景图	UPL_PNGFILE 					L305
1.2.6 激活/禁止系统	DIS_ENABLE 						L329
1.2.7 查询管理系统列表	QRY_SYSTEMLIST 				L352
2 用户注册
2.1 用户注册
2.1.1 注册名查重	QRY_USERNAME 						L391
2.1.2 获取短信验证码	GET_REGVRIFY 					L421
2.1.3 注册用户	SET_REGISTER 						L430
2.2	用户账号密码登录
2.2.1 获取短信验证码	GET_LOGVERIFY 					L457
2.2.2 用户登录	SET_LOGINWITHUNAME 					L465
2.3	用户TOKEN登录
2.3.1 用户登录	SET_LOGINWITHTOEKN 					L491
2.4 在线心跳
2.4.1 用户在线心跳信号(每15分钟一次)	SET_HEARTBEAT 	L515
2.5 退出登录
2.5.1 用户注销登录	SET_LOGOUT 						L525
3. 空间管理
3.1 管理员对空间管理
3.1.1 管理员查询已有的空间	QRY_AREA 				L537
3.1.2 管理员增加空间	ADD_AREA 						L573
3.1.2 管理员修改空间	MDF_AREA 						L610
3.1.3 管理员删除空间	DEL_AREA 						L643
4. 设备管理
4.1 主机管理
4.1.1 添加主机	ADD_HOST 							L674
4.1.2 修改主机	MDF_HOST 							L710
4.1.3 删除主机	DEL_HOST 							L747
4.1.4 查询主机	QRY_HOST 							L771
4.2 节点(控制器/执行器)管理
4.2.1 添加节点	ADD_NODE 							L817
4.2.2 修改节点	MDF_NODE 							L861
4.2.3 删除节点	DEL_NODE 							L907
4.2.4 查询节点	QRY_NODE 							L941
4.3 管理分站设备
4.3.1 添加分站	ADD_EQUIP 							L984
4.3.2 修改分站	MDF_EQUIP 							L1028
4.3.3 删除分站	DEL_EQUIP 							L1073
4.3.2 查询分站	QRY_EQUIP 							L1107
5. 定制管理(场景/任务管理)
5.1 任务定制
5.1.1 新增任务	ADD_TASK 							L1157
5.1.2 修改任务	MDF_TASK 							L1220
5.1.3 删除任务	DEL_TASK 							L1284
5.1.4 查询任务	QRY_TASK 							L1310
6. 操作管理
6.1 任务操作
6.1.1 设置任务运行模式	SET_TASKMODE 				L1376
6.1.2 查询任务运行模式	GET_TASKMODE 				L1403
6.1.3 查询系统下所有任务运行模式	GET_SYSTASK 		L1429
6.1.4 查询任务历史	GET_TASKHISTORY 				L1460
6.2 设备操作	
6.2.1 设置分站设备开关状态	SET_EQUIP 				L1496
6.2.2 查询分站设备开关状态	GET_EQUIP 				L1530
6.2.3 查询分站设备历史数据	GET_HISTSTATION 		L1563
6.3 节点操作	
6.3.1 节点激活/禁止	SET_NODEACTIVE 					L1606
6.3.2 节点休眠/唤醒	SET_NODEWAKEUP 					L1640
6.3.3 查询节点状态	GET_NODESTATUS 					L1674
6.3.4 查询节点历史数据	GET_NODEHISTORY 			L1717
6.3.5 查询节点历史状态	GET_NODESTATUSHISTORY 		L1758
7. 报告管理(用户登录立即报告, 以后每15分钟一次报告)
7.1 系统整体报告
7.1.1 气象报告	RPT_WHETHER 						L1798
7.1.2 系统简要报告	RPT_GENERAL 					L1807
7.2 分项报告
7.2.1 计划场景报告	RPT_TASKALL 					L1822
7.2.2 空间状态报告	RPT_AREAENV 					L1836
7.2.3 设备状态报告(每个devType设备种类分别报告)	RPT_EQUIPMENT 	L1851
8. 管理员对人员的管理 (用户注册后, 由管理员选择连接的系统)
8.1 查询人员	QRY_MEMBER
8.2 人员授权		QRY_MEMBER 							L1867
8.2.1 空间设备人员授权	SET_PERMIT 					L8197
8.2.2 查询人员-空间设备授权	QRY_PERMITMEMBER 		L1935
8.2.3 查询空间设备-人员授权	QRY_PERMITAREA 			L1977
反馈信息表											L2020


以下开始时JSON接口
--------------------------------------------------------------------------------------
1. 超级管理员
1.1 超级管理员登录
1.1.1 获取短信验证码
	{
		"todo",			"GET_SUPERVERIFY",
		"superName",	"superName",					// 必须填写
		"superPasswd",	"superPasswd",					// 必须填写 
		"needAnswer",	"yes"
	}

	返回成功
	{
		"what",			"GET_SUPERVERIFY",				// 表示收到请求
		"code",			"OK",
	}
	
1.1.2 超级管理员登录
	{
		"todo",			"SET_SUPERLOGIN",
		"superName",	"superName",					// 必须填写
		"superPasswd",	"superPasswd",					// 必须填写 
		"verifyCode",	"verifyCode",					// 短信验证码必须填写
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"SET_SUPERLOGIN",
		"code",			"0",
		"superID",		"superID"
	}

	返回失败
	{
		"what",			"SET_SUPERLOGIN",
		"code",			"3",
		"errNo",		"3",
		"errMsg",		"账号密码验证码错误"
	}

1.2 超级管理员新建修改激活禁止系统
1.2.1 系统和管理管账号查重	xx
	{
		"todo",			"QRY_SYSNAME",
		"superID",		"superID",						// superID 不得修改
		"dispSystem",	"dispName",						// 显示用名称，长度20个汉字，显示在用户平台
		"corpName",		"corpName",						// 单位名称，长度20个汉字，企业名称，不能重复
		"adminName",	"adminName",					// 用户管理员，管理该系统下内容，不能重复
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_SYSNAME",
		"code",			"0",
		"systemID",		"systemID",						// 系统赋予的编号，与单位名称相对应
		"adminID",		"adminID",						// 系统赋予的编号，与管理员名称相对应
	}
	
	返回失败1
	{
		"what",			"QRY_SYSNAME",
		"code",			"3",
		"errNo",		"4",
		"errMsg",		"此注册名已被用"
	}
	返回失败2
	{
		"what",			"QRY_SYSNAME",
		"code",			"3",
		"errNo",		"2",
		"errMsg",		"此单位名已被用"
	}

1.2.2 获取短信验证码	xx
	{
		"todo",			"GET_ADMINVERIFY",
		"superID",		"superID",						// superID 不得修改
		"adminName",	"adminName",					// 必须填写，长度10个汉字，
		"adminPasswd",	"adminPasswd",					// 必须填写，长度8为数字 
		"adminPhone",	"adminPhone",					// 必须填写手机号
		"needAnswer",	"yes"
	}

	返回成功
	{
		"what",			"GET_SUPERVERIFY",				// 表示收到请求
		"code",			"OK",
	}
	
1.2.3 新建单位和管理员	xx
	{
		"todo",			"ADD_NEWSYSTEM",
		"superID",		"superID",						// superID 不得修改
		"systemID",		"systemID",
		"corpName",		"corpName",
		"dispName",		"dispName",
		"adminID",		"adminID",
		"adminName",	"adminName",					// 用户管理员，管理该系统下内容，不能重复
		"adminPasswd",	"passwd",
		"adminPhoneNum",	"phoneNum",
		
		"adminVerifyCode",	"adminVerifyCode",			// 短信验证码必须填写
		
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"ADD_NEWSYSTEM",
		"code",			"0",
		"setupTime",	"setupTime"						// 设置成功，返回系统没时间，年月日时分秒毫秒
	}
	
	返回失败
	{
		"what",			"ADD_NEWSYSTEM",
		"code",			"3",
		"errNo",		"1",
		"errMsg",		"操作失败"
	}

1.2.4 修改系统
	{
		"todo",			"MDF_CURSYSTEM",
		"superID",		"superID",						// superID 不得修改

		"systemID",		"systemID",						// 系统赋予的编号，与单位名称相对应
		"dispSystem",	"dispName",						// 显示用名称，长度20个汉字，显示在用户平台
		"corpName",		"corpName",
		
		"adminID",		"adminID",
		"adminName",	"adminName",					// 用户管理员，管理该系统下内容，不能重复
		"adminPasswd",	"passwd",
		"adminPhoneNum",	"phoneNum",
		
		"adminVerifyCode",	"adminVerifyCode",			// 短信验证码必须填写

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"MDF_CURSYSTEM",
		"code",			"0",
		"setupTime",	"setupTime"						// 设置成功，返回系统没时间，年月日时分秒毫秒
	}
	
	返回失败
	{
		"what",			"MDF_CURSYSTEM",
		"code",			"3",
		"errNo",		"1",
		"errMsg",		"操作失败"
	}
	
1.2.5 上传网页背景图
	{
		"todo",			"UPL_PNGFILE",					// 图片分辨率 1920*1080
		"superID",		"superID",						// superID 不得修改

		"systemID",		"systemID",						// systemID 不得修改
		"pngFileName",	"pngFileName",					// 背景图将被保存到 /usr/local/nginx/html/usrimage
		"logoFileName",	"logoFileName",
		"pngFile",		"pngFile",
		"pngMD5",		"pngMD5",
		"logoMD5",		"logoMD5",
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"UPL_PNGFILE",
		"code",			"0",
		"fileToken",	"filetoken.png"					// 上传文件经过计算，转为token文件名，用以排重
		"logoToken",	"logotoken.png"					// 上传文件经过计算，转为token文件名，用以排重
	}
	
	返回失败
	{
		"what",			"UPL_PNGFILE",
		"code",			"3",
		"errNo",		"8",
		"errMsg",		"上传文件失败"
	}
	
1.2.6 激活/禁止系统
	{
		"todo",			"DIS_ENABLE",
		"superID",		"superID",						// superID 不得修改
		"systemID",		"systemID",						// systemID 不得修改
		"manage",		"DISABLE/ENABLE",				// DISABLE/ENABLE 二选一
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"DIS_ENABLE",
		"code",			"0",
		"setupTime",	"setupTime"						// 设置成功，返回系统没时间，年月日时分秒毫秒
	}
	
	返回失败
	{
		"what",			"DIS_ENABLE",
		"code",			"3",
		"errNo",		"1",
		"errMsg",		"操作失败"
	}
	
1.2.7 查询管理系统列表
	{
		"todo",			"QRY_SYSTEMLIST",
		"superID",		"superID",						// superID 不得修改
		"systemID",		"systemID",						// systemID 不得修改
		"first",		"first",						// 本次查询一个位置 个数, 从1开始
		"number",		"NUMBER",						// 本次返回 NUMBER 个数，0表示所有
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_SYSTEMLIST",
		"code",			"0",
		"number",		"number",						// 本次实际返回个数
		system["number"] {
			"systemID",		"systemID",					// 系统赋予的编号，与单位名称相对应
			"dispSystem",	"dispName",					// 显示用名称，长度20个汉字，显示在用户平台
			"corpName",		"corpName",
			
			"adminID",		"adminID",
			"adminName",	"adminName",				// 用户管理员，管理该系统下内容，不能重复
			"adminPhoneNum",	"phoneNum",

			"status",		"DISABLE/ENABLE",
			"setupTime",	"setupTime"					// 设置成功，返回系统没时间，年月日时分秒毫秒
		}
	}
	
	返回失败
	{
		"what",			"QRY_SYSTEMLIST",
		"code",			"3",
		"errNo",		"1",
		"errMsg",		"操作失败"
	}
	
--------------------------------------------------------------------------------------
2 用户注册登录
2.1 用户注册
2.1.1 注册名查重
	{
		"todo",			"QRY_USERNAME",
		"userName",		"userName",						// 用户注册名，全系统查重，必须填写
		"needAnswer", 	"yes"
	}
	
	返回成功
	{
		"what",			"QRY_USERNAME",
		"code",			"0",
		"userID",		"userID"						// 查重成功后，系统返回赋予的userID，不显示在界面
	}
	
	返回失败1
	{
		"what",			"QRY_USERNAME",
		"code",			"3",
		"errNo",		"4",
		"errMsg",		"此注册名已被用"
	}
	返回失败2
	{
		"what",			"QRY_USERNAME",
		"code",			"3",
		"errNo",		"7",
		"errMsg",		"此系统不存在"
	}

2.1.2 获取短信验证码
	{
		"todo",			"GET_REGVRIFY",
		"userName",		"userName",
		"userPhone",	"phoneNum",
		"password",		"password",
		"needAnswer",	"yes"
	}

	返回成功
	{
		"what",			"GET_REGVRIFY",					// 表示收到请求
		"code",			"OK",
	}
	
2.1.3 注册用户
	{
		"todo",			"SET_REGISTER",
		"userID",		"userID",						// 查重时，系统赋予
		"corpName",		"corpName",						// 单位名称，检查该单位存在
		"userName",		"userName",
		"userPhone",	"phoneNum",
		"password",		"password",
		"verifyCode",	"verifyCode",
		"needAnswer",	"yes"
	}
	
	返回成功
	{
		"what",			"SET_REGISTER",
		"code",			"0",
		"token",		"TOKEN"
	}
	
	返回失败
	{
		"what",			"SET_REGISTER",
		"code",			"3",
		"errNo",		"5",
		"errMsg",		"注册失败，请联系客服"
	}
	
2.2	(网页)用户账号密码登录
2.2.1 获取短信验证码
	{
		"todo",			"GET_LOGVERIFY",
		"userName",		"userName",
		"password",		"password",
		"needAnswer",	"no"
	}

2.2.2 用户登录
	{
		"todo",			"SET_LOGINWITHUNAME",
		"corpName",		"corpName",						
		"userName",		"userName",
		"password",		"password",
		"verifyCode",	"verifyCode",
		"needAnswer",	"yes"
	}
	
	返回成功
	{
		"what",			"SET_LOGINWITHUNAME",
		"code",			"0",
		"userID",		"userID",
		"token",		"TOKEN"
	}
	
	返回失败
	{
		"what",			"SET_LOGINWITHUNAME",
		"code",			"3",
		"errNo",		"6",
		"errMsg",		"登录失败，请联系客服"
	}
	
2.3	(手机)用户TOKEN登录
2.3.1 用户登录
	{
		"todo",			"SET_LOGINWITHTOEKN",
		"userID",		"userID",
		"token",		"TOKEN",
		"needAnswer",	"yes"
	}
	
	返回成功
	{
		"what",			"SET_LOGINWITHTOEKN",
		"code",			"0",
		"token",		"TOKEN"
	}
	
	返回失败
	{
		"what",			"SET_LOGINWITHTOEKN",
		"code",			"3",
		"errNo",		"6",
		"errMsg",		"登录失败，请联系客服"
	}

2.4 在线心跳
2.4.1 用户在线心跳信号(每15分钟一次)
	{
		"todo",			"SET_HEARTBEAT"
		"systemID",		"systemID",						
		"userID",		"userID",
		"token",		"TOKEN"
		"needAnswer", 	"no"
	}

2.5 退出登录
2.5.1 用户注销登录
	{
		"todo",			"SET_LOGOUT"
		"systemID",		"systemID",						
		"userID",		"userID",
		"token",		"TOKEN"
		"needAnswer", 	"no"
	}

--------------------------------------------------------------------------------------
3. 空间管理
3.1 管理员对空间管理
3.1.1 管理员查询已有的空间
	{
		"todo",			"QRY_AREA",
		"systemID",		"systemID",						
		"userID",		"userID",						// 管理员权限用户编号
		"token",		"TOKEN"

		"first",		"first",						// 本次查询一个位置 个数
		"number",		"number",						// number 本次返回人员， 0 表示所有
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_AREA",
		"code",			"0",
		"first",		"first",						// 返回的第一个记录号		
		"number",		"number",						// 本次返回记录个数
		area["number"] {
			"areaID",		"areaID",					// 空间序号，系统赋予
			"areaNo",		"areaNo",					// 空间编号，用户设置
			"areaName",		"areaName",					// 空间名称
			"areaLocation",	"areaLocation",				// 空间所在位置
			"areaValue",	"areaValue",				// 空间面积
			"areaHight",	"areaHight",				// 空间高度
			"memo",			"memo"						// 备注说明
		}
	}
	
	返回失败
	{
		"what",			"QRY_AREA",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

3.1.2 管理员增加空间
	{
		"todo",			"ADD_AREA",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"number",		"number",						// number 本次增加空间数量
		area["number"] {
			"areaNo",		"areaNo",					// 空间编号，用户设置
			"areaName",		"areaName",					// 空间名称
			"areaLocation",	"areaLocation",				// 空间所在位置
			"areaValue",	"areaValue",				// 空间面积
			"areaHight",	"areaHight"					// 空间高度
			"memo",			"memo"						// 备注说明
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"ADD_AREA",
		"code",			"0",
		"number",		"number",						// number 本次增加空间数量
		area["number"] {
			"areaID",		"areaID",					// 系统赋予的空间ID，不显示在界面
			"areaNo",		"areaNo",					// 空间编号，用户设置
		}
	}
	
	返回失败
	{
		"what",			"ADD_AREA",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

3.1.2 管理员修改空间
	{
		"todo",			"MDF_AREA",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"number",		"number",						// number 本次增加空间数量
		area["number"] {
			"areaID",		"areaID",					// 空间序号，用户不能修改
			"areaNo",		"areaNo",					// 空间编号，用户设置
			"areaName",		"areaName",					// 空间名称
			"areaLocation",	"areaLocation",				// 空间所在位置
			"areaValue",	"areaValue",				// 空间面积
			"areaHight",	"areaHight",				// 空间高度
			"memo",			"memo"						// 备注说明
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"MDF_AREA",
		"code",			"OK",
	}
	
	返回失败
	{
		"what",			"MDF_AREA",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

3.1.3 管理员删除空间
	{
		"todo",			"DEL_AREA",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"number",		"number",						// number 本次增加空间数量
		area["number"] {
			"areaID",		"areaID",					// 空间编号， 修改是不能为0
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"DEL_AREA",
		"code",			"OK",
	}
	
	返回失败
	{
		"what",			"DEL_AREA",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

--------------------------------------------------------------------------------------
4. 设备管理
4.1 主机管理
4.1.1 添加主机
	{
		"todo",			"ADD_HOST",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",						// 用户序号，不能修改
		"token",		"TOKEN"

		"devEUI",		"devEUI",						// 主机编号，物理主机在主机标牌上，虚拟主机填0，由云端赋值
		"hostType",		"SERVER/VIRTUAL",				// SERVER表示物理主机server mode，VIRTUAL为虚拟主机 serverless mode
		"hostNo",		"hostNo",						// 主机编号，虚拟主机为NULL
		"hostName",		"hostName",						// 主机名称，虚拟主机为NULL
		"memo",			"memo"							// 备注说明

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"ADD_HOST",
		"code",			"0",
		"hostID",		"hostID",						// 主机顺序号，由云端返回
		"devEUI",		"devEUI",						// 主机的设备号，物理主机为原值，虚拟主机位云端赋值
		"maxConnection",	"maxConnection"				// 可以连接设备的最大值, 虚拟主机为NULL
// 以下三项因设备而异		
		"location",		"location",						// 主机所在地址，虚拟主机为NULL
		"latitude",		"latitude",						// 经度，虚拟主机为NULL
		"longitude",	"longitude",					// 纬度，虚拟主机为NULL
	}
	
	返回失败
	{
		"what",			"ADD_HOST",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.1.2 修改主机
	{
		"todo",			"MDF_HOST",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机顺序号，由云端返回
		"hostNo",		"hostNo",						// 主机编号，用户设置
		"hostName",		"hostName",						// 主机名称，虚拟主机为NULL
		"devEUI",		"devEUI",						// 设备编号，物理主机在主机标牌上，虚拟主机填0，由云端赋值
		"hostType",		"SERVER/VIRTUAL",				// SERVER表示物理主机，VIRTUAL为虚拟主机
		"memo",			"memo"							// 备注说明

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"MDF_HOST",
		"code",			"0",
		"hostID",		"hostID",						// 主机顺序号，由云端返回
		"devEUI",		"devEUI",						// 主机的设备号，物理主机为原值，虚拟主机位云端赋值
		"maxConnection",	"maxConnection"				// 可以连接设备的最大值, 虚拟主机为NULL
// 以下三项因设备而异		
		"location",		"location",						// 主机所在地址，虚拟主机为NULL
		"latitude",		"latitude",						// 经度，虚拟主机为NULL
		"longitude",	"longitude",					// 纬度，虚拟主机为NULL
	}
	
	返回失败
	{
		"what",			"MDF_HOST",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.1.3 删除主机
	{
		"todo",			"DEL_HOST",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"
		"hostID",		"hostID",						// 主机序号
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"DEL_HOST",
		"code",			"OK",
	}
	
	返回失败
	{
		"what",			"DEL_HOST",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.1.4 查询主机
	{
		"todo",			"QRY_HOST",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"
//查询一，查询确定编号或名称的主机
		"number",		"number",						// 查询主机数量
		host["number"] {
			"hostNo",		"hostNo",					// 查询主机的编号
			"hostName",		"hostName",					// 查询主机的名称
		}
//查询二，查询不确定名称的主机
		"first",		"first",
		"number",		"number",
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_HOST",
		"code",			"0",
		"number",		"number"						// 查询返回数量
		host["number"] {
			"hostID",		"hostID",					// 主机序号
			"hostNo",		"hostNo",					// 主机编号
			"devEUI",		"devEUI",					// 设备编号，物理主机在主机标牌上，虚拟主机填0，由云端赋值
			"hostName",		"hostName",					// 主机名称，虚拟主机为NULL
			"hostType",		"SERVER/VIRTUAL",			// SERVER表示物理主机，VIRTUAL为虚拟主机
			"maxConnection",	"maxConnection"			// 可以连接设备的最大值, 虚拟主机为NULL
			"memo",			"memo"						// 备注说明
		}
	}
	
	返回失败
	{
		"what",			"QRY_HOST",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}


4.2 节点(控制器/执行器)管理
4.2.1 添加节点
	{
		"todo",			"ADD_NODE",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机序号
		"number",		"number"						// 本次添加节点数量，数量不能为0
		node["number"] {
			"nodeNo",		"nodeNo",					// 节点编号
			"devEUI",		"devEUI",					// 设备编号，在设备标牌上 
			"nodeName",		"nodeName",					// 节点名称
			"nodeType",		"nodeType",					// 节点类型
			"nodePort",		"nodePort",					// 节点端口数量，默认1
			"memo",			"memo"						// 备注说明
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"ADD_NODE",
		"code",			"0",
		"number",		"number",
		node["number"] {
			"nodeID",		"nodeID",						// 节点序号，有云端返回
			"devEUI",		"devEUI",						// 节点的设备号
		}
	}
	
	返回失败
	{
		"what",			"ADD_NODE",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.2.2 修改节点
	{
		"todo",			"MDF_NODE",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机序号
		"number",		"number"						// 保存添加节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点序号
			"nodeNo",		"nodeNo",					// 节点编号
			"devEUI",		"devEUI",					// 节点编号，在节点标牌上 
			"nodeName",		"nodeName",					// 节点名称
			"nodeType",		"nodeType",					// 节点类型
			"nodePort",		"nodePort",					// 节点端口数量，默认1
			"memo",			"memo"						// 备注说明
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"MDF_NODE",
		"code",			"0",
		"code",			"0",
		"number",		"number",
		node["number"] {
			"nodeID",		"nodeID",					// 节点序号，有云端返回
			"devEUI",		"devEUI",					// 设备编号
		}
	}
	
	返回失败
	{
		"what",			"MDF_NODE",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.2.3 删除节点
	{
		"todo",			"DEL_NODE",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机序号
		"number",		"number"						// 保存添加节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点序号
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"DEL_NODE",
		"code",			"OK",
	}
	
	返回失败
	{
		"what",			"DEL_NODE",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.2.4 查询节点(两种查询选一)
	{
		"todo",			"QRY_NODE",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机序号
// 查询一，查询指定节点		
		"nodeID",		"nodeID",						// 节点序号
// 查询二，全部查询		
		"first",		"first",						// 本次查询第一个节点位置
		"number",		"number"						// 本次查询数量, 0表示所有
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_NODE",
		"code",			"0",
		"number",		"number",
		"number",		"number"						// 保存添加节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点序号
			"nodeNo",		"nodeNo",					// 节点编号
			"devEUI",		"devEUI",					// 节点编号，在节点标牌上 
			"nodeName",		"nodeName",					// 节点名称
			"nodeType",		"nodeType",					// 节点类型
			"nodePort",		"nodePort",					// 节点端口数量，默认1
			"memo",			"memo"						// 备注说明
		}
	}
	
	返回失败
	{
		"what",			"QRY_NODE",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.3 管理分站设备
4.3.1 添加分站设备
	{
		"todo",			"ADD_EQUIP",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机序号
		"nodeID",		"nodeID",						// 节点序号
		"number",		"number"						// 本次添加分站数量，数量不能为0
		equip["number"] {
			"equipNo",		"equipNo",					// 设备编号
			"equipName",	"equipName",				// 设备名称
			"equipType",	"equipType",				// 设备类型，11空调、12照明、13电表、14插座、15水表、1阀门
			"portNo",		"portNo",					// 节点端口号
			"areID",		"areaID",					// 空间编号
			"memo",			"memo"						// 备注说明
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"ADD_EQUIP",
		"code",			"0",
		"number",		"number",
		equip["number"] {
			"equipID",		"equipID",					// 设备序号
			"equipNo",		"equipNo",					// 设备编号
		}
	}
	
	返回失败
	{
		"what",			"ADD_EQUIP",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.3.2 修改分站
	{
		"todo",			"MDF_EQUIP",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机序号
		"nodeID",		"nodeID",						// 节点序号
		"number",		"number"						// 本次添加分站数量，数量不能为0
		equip["number"] {
			"equipID",		"equipID",					// 设备序号
			"equipNo",		"equipNo",					// 设备编号
			"equipName",	"equipName",				// 分站命名
			"portNo",		"portNo",					// 节点端口号
			"areID",		"areaID",					// 空间编号
			"memo",			"memo"						// 备注说明
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"MDF_EQUIP",
		"code",			"OK",
	}
	
	返回失败
	{
		"what",			"MDF_EQUIP",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.3.3 删除分站
	{
		"todo",			"DEL_EQUIP",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机序号
		"nodeID",		"nodeID",						// 节点序号
		"number",		"number"						// 本次添加分站数量，数量不能为0
		equip["number"] {
			"equipID",		"equipID",					// 设备序号
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"DEL_EQUIP",
		"code",			"OK",
	}
	
	返回失败
	{
		"what",			"DEL_EQUIP",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

4.3.2 查询分站(三种查询选一种)
	{
		"todo",			"QRY_EQUIP",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"hostID",		"hostID",						// 主机序号
// 查询一，确定节点		
		"nodeID",		"nodeID",						// 节点序号
// 查询二，确定空间
		"areaID",		"areaID",						// 空间编号
// 查询三，全部查询		
		"first",		"first",
		"number",		"number"						// 本次添加分站数量，数量不能为0

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_EQUIP",
		"code",			"0",
		"number",		"number",
		equip["number"] {
			"equipID",		"equipID",					// 设备序号
			"equipNo",		"equipNo",					// 设备编号
			"equipName",	"equipName",				// 分站命名
			"portNo",		"portNo",					// 节点端口号
			"areID",		"areaID",					// 空间编号
			"memo",			"memo"						// 备注说明
		}
	}
	
	返回失败
	{
		"what",			"QRY_EQUIP",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

--------------------------------------------------------------------------------------
5. 定制管理(场景/任务管理)
5.1 任务定制
5.1.1 新增任务
	{
		"todo",			"ADD_TASK",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"areaID",		"areaID",						// 空间编号

		"taskNo",		"taskNo",						// 任务编号
		"taskName",		"taskName",						// 任务名称
		"taskType",		"TIMING/CYCLING/SENSOR/SCENERY",	// 任务种类，TIMING定时，CYCLING循环，SENSOR采集，SCENERY场景，选一
		"cycleNum",		"cycleNum",						// 循环次数，如果taskType为CYCLING时需要
		"action",		"TURN-ON/TURN_OFF/TURN_ADJ/COLLECT/ORDER", // 执行动作，TURN-ON打开，TURN-OFF关闭，TURN-ADJ调节，COLLECT采集，ORDER指令，选一
		"actOnTime",	"actOnTime",					// 动作持续时间，
		"setupDay",		"setupDay",						// 设置日
		"repeatMode",	"ODD_DAY/EVEN_DAY/INT_DAY/WORKDAY/WEEKEND/HOLIDAY/MANUAL",	
														// 循环模式，ODD_DAY奇数日，EVEN_DAY偶数日，INT_DAY间隔日，WORKDAY工作日，WEEKEND周末，HOLIDAY节假日，MANUAL手动设置，选一
		"intervalDay",	"intervalDay",					// 间隔天数，如果repeatMode为INT_DAY时需要
		"actDay",		"actDay",						// 动作日期，如果repeatMode为MANUAL时需要

		"number1",		"number1",						// 一天内动作次数，最多12次
		start["number1"] {
			"startTime",	"startTime",				// 开始时间，时分
		}

		"number2",		"number2",						// 相关传感参数数量，最多4项
		sense["number2"] {
			"highValue",	"highValue",				// 高程数值
			"highAct",		"TURN_ON/TURN_OFF",			// 高于高程时动作，二选一
			"lowValue",		"lowValue",					// 低程数值
			"lowAct",		"TURN_ON/TURN_OFF",			// 低于低程时动作，二选一
		}

		"number3",		"number3",						// 被选分站数量
		equip["number3"] {
			"equipID",		"equipID",					// 被选设备列表
		}
		"concurrent",	"concurrent",					// 同时动作的设备数量

		"memo",			"memo",							// 备注说明

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"ADD_TASK",
		"code",			"0",
		"taskID",		"taskID",						// 任务序号
		"taskNo",		"taskNo",						// 任务编号
	}
	
	返回失败
	{
		"what",			"ADD_TASK",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

5.1.2 修改任务
	{
		"todo",			"MDF_TASK",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"areaID",		"areaID",						// 空间编号

		"taskID",		"taskID",						// 任务序号
		"taskNo",		"taskNo",						// 任务编号
		"taskName",		"taskName",						// 任务名称
		"taskType",		"TIMING/CYCLING/SENSOR/SCENERY",	// 任务种类，TIMING定时，CYCLING循环，SENSOR采集，SCENERY场景，选一
		"cycleNum",		"cycleNum",						// 循环次数，如果taskType为CYCLING时需要
		"action",		"TURN-ON/TURN_OFF/TURN_ADJ/COLLECT/ORDER", // 执行动作，TURN-ON打开，TURN-OFF关闭，TURN-ADJ调节，COLLECT采集，ORDER指令，选一
		"actOnTime",	"actOnTime",					// 动作持续时间，
		"setupDay",		"setupDay",						// 设置日
		"repeatMode",	"ODD_DAY/EVEN_DAY/INT_DAY/WORKDAY/WEEKEND/HOLIDAY/MANUAL",	
														// 循环模式，ODD_DAY奇数日，EVEN_DAY偶数日，INT_DAY间隔日，WORKDAY工作日，WEEKEND周末，HOLIDAY节假日，MANUAL手动设置，选一
		"intervalDay",	"intervalDay",					// 间隔天数，如果repeatMode为INT_DAY时需要
		"actDay",		"actDay",						// 动作日期，如果repeatMode为MANUAL时需要

		"number1",		"number1",						// 一天内动作次数，最多12次
		start["number1"] {
			"startTime",	"startTime",				// 开始时间，时分
		}

		"number2",		"number2",						// 相关传感参数数量，最多4项
		sense["number2"] {
			"highValue",	"highValue",				// 高程数值
			"highAct",		"TURN_ON/TURN_OFF",			// 高于高程时动作，二选一
			"lowValue",		"lowValue",					// 低程数值
			"lowAct",		"TURN_ON/TURN_OFF",			// 低于低程时动作，二选一
		}

		"number3",		"number3",						// 被选分站数量
		equip["number3"] {
			"equipID",		"equipID",					// 被选设备列表
		}
		"concurrent",	"concurrent",					// 同时动作的设备数量

		"memo",			"memo",							// 备注说明

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"MDF_TASK",
		"code",			"0",
		"taskID",		"taskID",						// 任务序号
		"taskNo",		"taskNo",						// 任务编号
	}
	
	返回失败
	{
		"what",			"MDF_TASK",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

5.1.3 删除任务
	{
		"todo",			"DEL_TASK",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"
		"taskID",		"taskID",						// 任务顺序号
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"DEL_TASK",
		"code",			"OK",
	}
	
	返回失败
	{
		"what",			"DEL_TASK",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

5.1.4 查询任务
	{
		"todo",			"QRY_TASK",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"areaID",		"areaID",						// 空间编号，为空，查询系统中所有任务，不为空，查询指定空间内任务
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_TASK",
		"code",			"0",
		"number",		"number",						// 本次返回任务数量
		task["number"] {
			"taskID",		"taskID",						// 任务序号
			"taskNo",		"taskNo",						// 任务编号
			"taskName",		"taskName",						// 任务名称
			"taskType",		"TIMING/CYCLING/SENSOR/SCENERY",	// 任务种类，TIMING定时，CYCLING循环，SENSOR采集，SCENERY场景，选一
			"cycleNum",		"cycleNum",						// 循环次数，如果taskType为CYCLING时需要
			"action",		"TURN-ON/TURN_OFF/TURN_ADJ/COLLECT/ORDER", // 执行动作，TURN-ON打开，TURN-OFF关闭，TURN-ADJ调节，COLLECT采集，ORDER指令，选一
			"actOnTime",	"actOnTime",					// 动作持续时间，
			"setupDay",		"setupDay",						// 设置日
			"repeatMode",	"ODD_DAY/EVEN_DAY/INT_DAY/WORKDAY/WEEKEND/HOLIDAY/MANUAL",	
															// 循环模式，ODD_DAY奇数日，EVEN_DAY偶数日，INT_DAY间隔日，WORKDAY工作日，WEEKEND周末，HOLIDAY节假日，MANUAL手动设置，选一
			"intervalDay",	"intervalDay",					// 间隔天数，如果repeatMode为INT_DAY时需要
			"actDay",		"actDay",						// 动作日期，如果repeatMode为MANUAL时需要

			"number1",		"number1",						// 一天内动作次数，最多12次
			start["number1"] {
				"startTime",	"startTime",				// 开始时间，时分
			}

			"number2",		"number2",						// 相关传感参数数量，最多4项
			sense["number2"] {
				"highValue",	"highValue",				// 高程数值
				"highAct",		"TURN_ON/TURN_OFF",			// 高于高程时动作，二选一
				"lowValue",		"lowValue",					// 低程数值
				"lowAct",		"TURN_ON/TURN_OFF",			// 低于低程时动作，二选一
			}

			"number3",		"number3",						// 被选分站数量
			equip["number3"] {
				"equipID",		"equipID",					// 被选设备列表
			}
			"concurrent",	"concurrent",					// 同时动作的设备数量

			"memo",			"memo",							// 备注说明
		}
	}
	
	返回失败
	{
		"what",			"QRY_TASK",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

--------------------------------------------------------------------------------------
6. 操作管理
6.1 任务操作
6.1.1 设置任务运行模式
	{
		"todo",			"SET_TASKMODE",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN",
		"taskID",		"taskID",						// 任务顺序号
		"runMode",		"MANUAL/STOP/AUTO",				// MANUAL手动，STOP手动，AUTO自动， 三选一
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"SET_TASKMODE",
		"code",			"0",
		"taskID",		"taskID",						// 任务顺序号
		"runMode",		"MANUAL/STOP/AUTO",				// MANUAL手动，STOP手动，AUTO自动
	}
	
	返回失败
	{
		"what",			"SET_TASKMODE",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}
	
6.1.2 查询任务当前运行模式
	{
		"todo",			"GET_TASKMODE",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"
		"taskID",		"taskID",						// 任务顺序号
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"GET_TASKMODE",
		"code",			"0",
		"taskID",		"taskID",						// 任务顺序号
		"runMode",		"MANUAL/STOP/AUTO",				// MANUAL手动，STOP手动，AUTO自动
	}
	
	返回失败
	{
		"what",			"GET_TASKMODE",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

6.1.3 查询系统下所有任务运行模式
	{
		"todo",			"GET_SYSTASK",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"
		"first",		"first",						// 本次查询的首记录
		"number",		"number",						// 本次查询个数，0为全部
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"GET_SYSTASK",
		"code",			"0",
		"first",		"first"
		"number",		"number",
		task["number"] {
			"taskID",		"taskID",						// 任务顺序号
			"runMode",		"MANUAL/STOP/AUTO",				// MANUAL手动，STOP手动，AUTO自动
		}
	}
	
	返回失败
	{
		"what",			"GET_SYSTASK",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}
	
6.1.4 查询任务历史
	{
		"todo",			"GET_TASKHISTORY",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"taskID",		"taskID",						// 任务顺序号
		"qureyMode",	"WEEK/MONTH/QUATER/YEAR/DAYS",	// 查询模式, WEEK为1周7天，MONTH为1月依月份，QUATER为季度，YEAR为年，DAYS为设置开始和结束日
		"beginDay",		"beginDay",						// 开始日
		"endDay",		"endDay",						// 结束日

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"GET_TASKHISTORY",
		"code",			"0",
		"days",			"days",							// 返回的数据组数量，同一时间所有的参数为一组，days表示有多少天数据
		day["days"] {
			"recvTime",		"recvTime",					// 动作时间
			"runMode",		"runMode",					// 动作状态
		}
	}
	
	返回失败
	{
		"what",			"GET_TASKHISTORY",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}


6.2 设备操作	
6.2.1 设置设备开关状态
	{
		"todo",			"SET_EQUIP",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"number",		"number",						// 本次开关设备数量
		equip["number"] {
			"equipID",		"equipID",					// 设备序号
			"runMode",		"TURN-ON/TURN-OFF",			// TURN-ON、TURN-OFF， 二选一
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"SET_EQUIP",
		"code",			"0",
		"number",		"number",						// 本次开关设备数量
		equip["number"] {
			"equipID",		"equipID",					// 设备序号
			"status",		"status",					// 执行后设备状态
		}
	}
	
	返回失败
	{
		"what",			"SET_EQUIP",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

6.2.2 查询设备开关状态
	{
		"todo",			"GET_EQUIP",
		"systemID",		"systemID",						// systemID 不得空缺
		"userID",		"userID",
		"token",		"TOKEN"
		"areaID",		"areaID",						// 空间编号，为0，表示查询系统下所有设备状态
		"devType",		"devType",						// 设备类型，为‘空’，表示所有类型的设备
		"first",		"first",						// 本次查询的首记录
		"number",		"number",						// 本次查询个数，0为全部
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"_EQUIP",
		"code",			"0",
		"first",		"first"
		"number",		"number",
		equip["number"] {
			"equipID",		"equipID",					// 设备序号
			"status",		"TURN-ON/TURN-OFF",			// 当前设备状态
		}
	}
	
	返回失败
	{
		"what",			"_EQUIP",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}
	
6.2.3 查询分站设备历史数据
	{
		"todo",			"GET_EQUIPHISTORY",
		"systemID",		"systemID",						// systemID 不得空缺
		"userID",		"userID",
		"token",		"TOKEN"

		"areaID",		"areaID",						// 空间编号，不得为空
		"devType",		"devType",						// 设备类型，不得为空
		"number",		"number",						// 本次查询设备数量，不能等于0，大于1取所选设备的返回数据的平均值
		equip["number"] {
			"equipID",		"equipID",					// 设备序号
		}
		"qureyMode",	"WEEK/MONTH/QUATER/YEAR/DAYS",	// 查询模式, WEEK为1周7天，MONTH为1月依月份，QUATER为季度，YEAR为年，DAYS为设置开始和结束日
		"beginDay",		"beginDay",						// 开始日
		"endDay",		"endDay",						// 结束日

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"GET_EQUIPHISTORY",
		"code",			"0",
		"paramNum",		"paramNum",						// 返回的参数个数，根据设备而定，
		"days",			"days",							// 返回的数据天数，days表示有多少天数据
		day["days"] {
			"datetime",		"datetime",					// 数据时间，WEEK为日时分秒，month、QUATER、YEAR为月日
			param["paramNum"] {
				"param",	"param",					// 返回数据，图形表示颜色，0黑色，1红色，2绿色，3黄色，4蓝色，5洋红，6青色，7白色
			}
		}
	}
	
	返回失败
	{
		"what",			"GET_EQUIPHISTORY",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

6.3 节点操作	
6.3.1 节点激活/禁止
	{
		"todo",			"SET_NODEACTIVE",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"number",		"number",						// 本次操作节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点序号
			"runMode",		"ENABLE/DISABLE",			// ENABLE、DISABLE， 二选一，DISPABLE后节点自动休眠
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"SET_NODEACTIVE",
		"code",			"0",
		"number",		"number",						// 本次操作节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点编号
			"status",		"status",					// 执行后节点状态
		}
	}
	
	返回失败
	{
		"what",			"SET_NODEACTIVE",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

6.3.2 节点休眠/唤醒
	{
		"todo",			"SET_NODEWAKEUP",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"number",		"number",						// 本次操作节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点编号
			"runMode",		"WAKEUP/SLEEP",				// wakeup，SLEEP， 二选一，ENABLE后节点需要WAKEUP才能工作
		}
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"SET_NODEWAKEUP",
		"code",			"0",
		"number",		"number",						// 本次操作节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点编号
			"status",		"status",					// 执行后节点状态
		}
	}
	
	返回失败
	{
		"what",			"SET_NODEWAKEUP",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}
	
6.3.3 查询节点状态(两种查询选一种)
	{
		"todo",			"GET_NODESTATUS",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"
// 查询一，查询确定的节点
		"number1",		"number1",						// 本次操作节点数量
		node["number1"] {
			"nodeID",		"nodeID",					// 节点序号
		}
// 查询二，查询全部节点		
		"first",		"first",						// 本次查询第一个位置
		"number2",		"number2",						// 本次查询数量，0表示查询所有

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"GET_NODESTATUS",
		"code",			"0",
		"first",		"first",
		"number",		"number",						// 本次操作节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点编号
			"status",		"status",					// 执行后节点状态
// 以下4项因设备而异			
			"powerVoltage",	"powerVoltage",				// 系统电压，单位V
			"loadCurrent",	"loadCurrent",				// 负载电流，单位A
			"rssi",			"rssi",						// 信号强度，单位dbm
			"snr",			"snr",						// 信噪比
		}
	}
	
	返回失败
	{
		"what",			"GET_NODESTATUS",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

6.3.4 查询节点历史数据
	{
		"todo",			"GET_NODEHISTORY",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"number",		"number",						// 本次操作节点数量，number大于1，返回多个节点参数的平均值
		node["number"] {
			"nodeID",		"nodeID",					// 节点编号
		}
		"qureyMode",	"WEEK/MONTH/QUATER/YEAR/DAYS",	// 查询模式, WEEK为1周7天，MONTH为1月依月份，QUATER为季度，YEAR为年，DAYS为设置开始和结束日
		"beginDay",		"beginDay",						// 开始日
		"endDay",		"endDay",						// 结束日

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"GET_NODEHISTORY",
		"code",			"0",
		"days",			"days",							// 返回的数据天数，days表示有多少天数据
		day["days"] {
			"datetime",		"datetime",					// 数据时间，WEEK为日时分秒，month、QUATER、YEAR为月日
// 以下4项因设备而异			
			"powerVoltage",	"powerVoltage",				// 系统电压，单位V
			"loadCurrent",	"loadCurrent",				// 负载电流，单位A
			"rssi",			"rssi",						// 信号强度，单位dbm
			"snr",			"snr",						// 信噪比
		}
	}
	
	返回失败
	{
		"what",			"GET_NODEHISTORY",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}
	
6.3.5 查询节点历史状态
	{
		"todo",			"GET_NODESTATUSHISTORY",
		"systemID",		"systemID",						// systemID 不得修改
		"userID",		"userID",
		"token",		"TOKEN"

		"number",		"number",						// 本次操作节点数量
		node["number"] {
			"nodeID",		"nodeID",					// 节点编号
		}
		"qureyMode",	"WEEK/MONTH/QUATER/YEAR/DAYS",	// 查询模式, WEEK为1周7天，MONTH为1月依月份，QUATER为季度，YEAR为年，DAYS为设置开始和结束日
		"beginDay",		"beginDay",						// 开始日
		"endDay",		"endDay",						// 结束日

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"GET_NODESTATUSHISTORY",
		"code",			"0",
		"days",			"days",							// 返回的数据天数，days表示有多少天数据
		day["days"] {
			"datetime",		"datetime",					// 数据时间，单位年月日时分秒
			"status",		"DISABLE/SLEEP/WAKEUP",		// DISPABLE、SLEEP、WAKEUP, 三选一
		}
	}
	
	返回失败
	{
		"what",			"GET_NODESTATUSHISTORY",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

--------------------------------------------------------------------------------------
7. 报告管理(用户登录立即报告, 以后每15分钟一次报告)
7.1 系统整体报告
7.1.1 气象报告
	{
		"what",			"RPT_WHETHER"					// 今日天气
		"code",			"PUBLISH",
		"publish_time",	"publish_time",					// 发布时间，单位年月日时分秒
		"temperature",	"temp",							// 温度，单位℃
		"humidity",		"humidity",						// 湿度，单位Rh
	}
	
7.1.2 系统简要报告
	{
		"what",			"RPT_GENERAL"
		"code",			"PUBLISH",
		"publish_time",	"publish_time",					// 发布时间，单位年月日时分秒
		"energy_all",	"energy_all",					// 从零点至现在用电量
		"water_all",	"water_all",					// 从零点至现在用水量
		"equip_all",	"equip_all",					// 设备总数量
		"online_all",	"online_all",					// 在线设备总数量
		"running_all",	"running_all",					// 运行中设备总数量
		"task_all",		"task_all",						// 系统有预编计划总数量
		"ex_task_all",	"ex_task_all",					// 在执行中的计划总数量
	}
	
7.2 分项报告
7.2.1 计划场景报告
	{
		"what",			"RPT_TASKALL",
		"code",			"PUBLISH",
		"publish_time",	"publish_time",					// 发布时间，单位年月日时分秒
		"number",		"number",						// 计划数量
		task["number"] {
			"taskID",		"taskID",					// 计划编号
			"status",		"status",					// 计划当前状态
			"startTime",	"startTime",				// 状态开始时间
			"finishTime",	"finishTime",				// 状态结束时间
		}
	}

7.2.2 空间状态报告
	{
		"what",			"RPT_AREAENV"
		"code",			"PUBLISH",
		"publish_time",	"publish_time",					// 发布时间，单位年月日时分秒
		"number",		"number",						// 计划数量
		area["number"] {
			"areaID",		"areaID",
			"temperature",	"temp",						// 温度，单位℃
			"humidity",		"humidity",					// 湿度，单位Rh
			"brightness",	"brightness",				// 亮度，单位lux
			"turbidity",	"turbidity",				// 空气浑浊度，主要指二氧化碳浓度
		}
	}

7.2.3 设备状态报告(每个devType设备种类分别报告)
	{
		"what",			"RPT_EQUIPMENT"
		"code",			"PUBLISH",
		"publish_time",	"publish_time",					// 发布时间，单位年月日时分秒
		"devType",		"devType",						// 设备种类
		"number",		"number",						// 设备数量
		equip["number"] {
			"equipID",		"equipID",					// 设备编号
			"status",		"TURN-ON/TURN-OFF",			// 当前状态，TURN-ON、TURN-OFF二选一
			"areaID",		"areaID",					// 空间编号
		}
	}

--------------------------------------------------------------------------------------
8. 人员管理 
8.1 查询人员
	{
		"todo",			"QRY_MEMBER",
		"token",		"TOKEN"
		"systemID",		"systemID",						// systemID 不得修改
		"adminID",		"adminID",						// adminID 不得修改
		"first",		"first",						// 本次查询一个位置 个数
		"number",		"number",						// number 本次返回人员， 0 表示所有
		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_MEMBER",
		"code",			"0",
		"number",		"number"
		member["number"] {
			"userID",		"userID",
		}
	}
	
	返回失败
	{
		"what",			"QRY_MEMBER",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

8.2 人员授权
8.2.1 空间设备人员授权
	{
		"todo",			"SET_PERMIT",
		"token",		"TOKEN"
		"systemID",		"systemID",						// systemID 不得修改
		"adminID",		"adminID",						// adminID 不得修改
		
		"number1",		"number1",						// 被授权人员数量
		member["number1"] {
			"userID",		"userID",					// 被授权人员ID
			"number2",		"number2",					// 授权空间数量
			area["number2"] {
				"areaID",		"areaID",				// 被授权空间序号
				"number3",		"number3",				// 被授权设备数量
				equip["number3"] {
					"equipID",		"euipID",			// 被授权设备序号
					"permit",		"permit",			// 授权，R=RUN运行，V=VIEW查看，N=NONE无权限
				}
			}
		}

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"SET_PERMIT",
		"code",			"OK",
	}
	
	返回失败
	{
		"what",			"SET_PERMIT",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

8.2.2 查询人员-空间设备授权
	{
		"todo",			"QRY_PERMITMEMBER",
		"token",		"TOKEN"
		"systemID",		"systemID",						// systemID 不得修改
		"adminID",		"adminID",						// adminID 不得修改
		
		"number1",		"number1",						// 被授权人员数量
		member["number1"] {
			"userID",		"userID",					// 被授权人员ID
		}

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_PERMITMEMBER",
		"code",			"0",
		"number1",		"number1",						// 被授权人员数量
		member["number1"] {
			"userID",		"userID",					// 被授权人员ID
			"number2",		"number2",					// 授权空间数量
			area["number2"] {
				"areaID",		"areaID",				// 被授权空间序号
				"number3",		"number3",				// 被授权设备数量
				equip["number3"] {
					"equipID",		"euipID",			// 被授权设备序号
					"permit",		"R/V/N",			// 授权，R=RUN运行，V=VIEW查看，N=NONE无权限，三选一
				}
			}
		}
	}
	
	返回失败
	{
		"what",			"QRY_PERMITMEMBER",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

8.2.3 查询空间设备-人员授权
	{
		"todo",			"QRY_PERMITAREA",
		"token",		"TOKEN"
		"systemID",		"systemID",						// systemID 不得修改
		"adminID",		"adminID",						// adminID 不得修改
		
		"number1",		"number1",						// 被授权空间数量
		area["number1"] {
			"areaID",		"areaID",					// 被授权人员ID
		}

		"needAnswer", 	"yes"
	}

	返回成功
	{
		"what",			"QRY_PERMITAREA",
		"code",			"0",
		"number1",		"number1",						// 被授权空间数量
		area["number1"] {
			"areaID",		"areaID",					// 被授权空间编号
			"number2",		"number2",					// 授权空间数量
			equip["number2"] {
				"equipID",		"euipID",				// 空间设备列表
				"number3",		"number3",				// 被授权人员数量
				member["number3"] {
					"userID",		"userID",			// 被授权人员ID
					"permit",		"R/V",				// 授权，R=RUN运行，V=VIEW查看，二选一，N=NONE无权限不返回
				}
			}
		}
	}
	
	返回失败
	{
		"what",			"QRY_PERMITAREA",
		"code",			"3",
		"errNo",		"errNo",						// 返回错误号
		"errMsg",		"errMsg"						// 返回错误信息
	}

--------------------------------------------------------------------------------------
反馈信息列表
0,	OK
1,	操作失败
2,	此单位名已被用
3,	账号密码验证码错误
4,	此注册名已被用
5,	注册失败，请联系客服
6,	登录失败，请联系客服
7,	此系统不存在
8,	上传文件失败

--------------------------------------------------------------------------------------
