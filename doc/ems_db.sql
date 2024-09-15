CREATE DATABASE IF NOT EXISTS ems;
USE ems;

CREATE TABLE network_conf ( -- '系统-网络-云服-主机定义'
	system_type		CHAR(5) DEFAULT 'HOST' CHECK (system_type IN ('CLOUD', 'HOST')) COMMENT 'cloud or host',
	host_type		CHAR(10) DEFAULT 'PHYSIC' CHECK (host_type IN ('PHYSIC', 'VIRTUAL')) COMMENT 'physic or virtual',
	
	uplink_url		VARCHAR(50) COMMENT '上行地址：云服域名',
	remote_port		INTEGER COMMENT '云服-主机端口',

	local_ip		VARCHAR(16) COMMENT '下行地址：本机IP',
	web_port		INTEGER COMMENT '本机web端口',
	lora_port		INTEGER COMMENT '本机lora端口',
	net_mask		VARCHAR(16) COMMENT '局网掩码',
	local_gateway	VARCHAR(16) COMMENT '局网网关',
	
	datasource_ip	VARCHAR(50) COMMENT '数据库地址',
	datasource_port	INTEGER COMMENT '数据库端口',	
	datasource_usr	VARCHAR(10) COMMENT 'database admin',
	datasource_pwd	VARCHAR(10) COMMENT 'database password',
	dataschema		VARCHAR(10) COMMENT 'database schema',
	datacharset		VARCHAR(10) COMMENT 'database charset',
		
	memo			VARCHAR(255) COMMENT '备注说明'
) ENGINE = InnoDB;

CREATE TABLE ret_msg (
	ret_no			INTEGER PRIMARY KEY COMMENT '返回编号',
	ret_msg			VARCHAR(255) COMMENT '返回信息'
) ENGINE = InnoDB;

CREATE TABLE verify_code (
	verify_time		DATETIME(6) PRIMARY KEY COMMENT '校验时间',
	user_name		VARCHAR(50) COMMENT '账号名称',
	user_passwd		VARCHAR(10) COMMENT '密码',
	phone_no		BIGINT COMMENT '手机号码',
	verify_code		CHAR(7) COMMENT '校验码'
) ENGINE = InnoDB;

CREATE TABLE equip_param_def (
	param_no		INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '设备参数编号',
	param_name		VARCHAR(50) UNIQUE COMMENT '设备参数名称',
	uint			VARCHAR(10) COMMENT '设备参数单位'
) ENGINE = InnoDB;

-- supervisor define
CREATE TABLE supervisor_def (
	super_id		INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '超级管理员序号',
	super_name		VARCHAR(50) UNIQUE COMMENT '超级管理员账号',
	super_passwd	VARCHAR(10) COMMENT '密码',
	phone_no		BIGINT COMMENT '11位电话'
) ENGINE = InnoDB;

-- system define
CREATE TABLE system_def (
	system_id		INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '系统序号',
	corp_name		VARCHAR(100) UNIQUE COMMENT '单位名称',
	disp_name		VARCHAR(100) COMMENT '显示系统名称',
	create_day		DATETIME COMMENT '系统创建时间',
	modify_day		DATETIME COMMENT '系统修改时间',
	background_file	VARCHAR(255) COMMENT '背景文件',
	logo_file		VARCHAR(255) COMMENT '司标文件',
	back_fileMD5	VARCHAR(255) COMMENT '背景文件MD5',
	logo_fileMD5	VARCHAR(255) COMMENT '司标文件MD5',
	skin_no			INTEGER COMMENT '皮肤选择',
	system_status	CHAR(1) DEFAULT 'E' CHECK (system_status IN ('E', 'D')) COMMENT 'E激活、D禁止',
	memo			VARCHAR(255) COMMENT '备注说明'
) ENGINE = InnoDB;

CREATE TABLE super_system_map (
	super_id		INTEGER NOT NULL COMMENT '超级管理员序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	PRIMARY KEY (system_id, super_id),
	FOREIGN KEY (super_id) REFERENCES supervisor_def(super_id),
	FOREIGN KEY (system_id) REFERENCES system_def(system_id)
) ENGINE = InnoDB;

CREATE TABLE user_def (
	user_id			INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '人员序号',
	user_name		VARCHAR(50) UNIQUE COMMENT '账号名称',
	passwd			VARCHAR(10) COMMENT '密码6位数字',
	user_phone		BIGINT COMMENT '11位手机号码',
	wechart_no		VARCHAR(50) COMMENT '微信号',
	register_date	DATETIME COMMENT '注册时间',
	last_logintime	DATETIME COMMENT '最近登录时间',
	token			CHAR(129) COMMENT '系统赋予令牌，user_name+user_phone，last_logintime'
) ENGINE = InnoDB;

CREATE TABLE user_system_map (
	user_id			INTEGER NOT NULL COMMENT '人员序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	setup_time		DATETIME COMMENT '设置时间',
	permition		CHAR(1) DEFAULT 'N' CHECK (permition IN ('A','O','V','N')) COMMENT '权限，A管理员，O操作员，V观察员，N无权限',
	PRIMARY KEY (user_id, system_id),
	FOREIGN KEY (user_id) REFERENCES user_def(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE host_def (
	host_id			INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '主机序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	dev_eui			CHAR(65) UNIQUE COMMENT '设备唯一号',
	host_no			VARCHAR(10) NOT NULL COMMENT '主机编号',
	host_name		VARCHAR(50) COMMENT '主机名称',
	host_type		CHAR(1) DEFAULT 'P' CHECK (host_type IN ('P', 'V')) COMMENT '主机类型，P物理主机，V虚拟主机',
	location		VARCHAR(100) COMMENT '安装地点',
	latitude		CHAR(12) COMMENT '经度',
	logitude		CHAR(12) COMMENT '纬度',
	max_connection	INTEGER COMMENT '最多连接设备数量',
	register_time	DATETIME(6) COMMENT '注册时间',
	last_login_time	DATETIME(6) COMMENT '最近登录时间',
	token			CHAR(129) COMMENT '系统赋予令牌，dev_eui+host_type，last_login_time',
	memo			VARCHAR(255) COMMENT '备注说明',
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE host_history (
	host_id			INTEGER NOT NULL COMMENT '主机序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	recv_time		DATETIME(6) COMMENT '接收时间',
	status			VARCHAR(10) COMMENT '主机状态',
	PRIMARY KEY (recv_time, host_id),
	FOREIGN KEY (host_id) REFERENCES host_def(host_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE node_def (
	node_id			INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '节点序号',
	host_id			INTEGER NOT NULL COMMENT '主机序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	node_no			VARCHAR(10) NOT NULL COMMENT '节点编号',
	dev_eui			CHAR(65) UNIQUE COMMENT '节点唯一号',
	node_name		VARCHAR(50) COMMENT '节点名称',
	node_type		CHAR(1) COMMENT '节点类型',
	node_port		INTEGER CHECK (node_port > 0) COMMENT '节点端口数量',
	uplink_addr		INTEGER COMMENT '节点上联通讯地址',
	uplink_param	INTEGER COMMENT '节点上联通讯参数',
	downlink_addr	INTEGER COMMENT '节点下联地址',
	download_param	INTEGER COMMENT '节点下联通讯参数',
	memo			VARCHAR(255) COMMENT '备注说明',
	FOREIGN KEY (host_id) REFERENCES host_def(host_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE node_history (
	node_id			INTEGER NOT NULL COMMENT '节点序号',
	host_id			INTEGER NOT NULL COMMENT '主机序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	recv_time		DATETIME(6) COMMENT '接收时间',
	status			VARCHAR(10) COMMENT '节点状态',
	power_voltage	DOUBLE COMMENT '系统电压',
	load_current	DOUBLE COMMENT '负载电流',
	rssi			INTEGER COMMENT '信号强度',
	snr				DOUBLE COMMENT '信噪比',
	PRIMARY KEY (node_id, recv_time),
	FOREIGN KEY (node_id) REFERENCES node_def(node_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (host_id) REFERENCES host_def(host_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE equip_def (
	equip_id		INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '设备序号',
	node_id			INTEGER NOT NULL COMMENT '节点序号',
	host_id			INTEGER NOT NULL COMMENT '主机序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	equip_no		VARCHAR(10) NOT NULL COMMENT '设备编号',
	equip_name		VARCHAR(50) COMMENT '设备名称',
	port_no			INTEGER COMMENT '节点端口号',
	equip_type		VARCHAR(1) COMMENT '设备类型，空调、照明',
	drive_type		VARCHAR(1) COMMENT '设备驱动类型，单稳态、双稳态、三态、MB采集、AD采集、脉冲采集',
	drive_time		INTEGER COMMENT '驱动时间，单位毫秒',
	mb_addr			INTEGER COMMENT 'ModBus通讯地址',
	mb_param		INTEGER COMMENT 'ModBus通讯参数',
	memo			VARCHAR(255) COMMENT '备注说明',
	FOREIGN KEY (node_id) REFERENCES node_def(node_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (host_id) REFERENCES host_def(host_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE equip_history (
	equip_id		INTEGER NOT NULL COMMENT '设备序号',
	node_id			INTEGER NOT NULL COMMENT '节点序号',
	host_id			INTEGER NOT NULL COMMENT '主机序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	recv_time		DATETIME(6) COMMENT '接收时间',
	PRIMARY KEY (recv_time, equip_id),
	FOREIGN KEY (equip_id) REFERENCES equip_def(equip_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (node_id) REFERENCES node_def(node_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (host_id) REFERENCES host_def(host_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE equip_history_detail (
	equip_id		INTEGER NOT NULL COMMENT '设备序号',
	node_id			INTEGER NOT NULL COMMENT '节点序号',
	host_id			INTEGER NOT NULL COMMENT '主机编号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	data_seq		INTEGER NOT NULL COMMENT '数据顺序号',
	recv_time		DATETIME(6) COMMENT '接收时间',
	param_no		INTEGER  COMMENT '参数编号',		
	data_value		DOUBLE COMMENT '数据值',
	PRIMARY KEY (recv_time, equip_id, data_seq),
	FOREIGN KEY (equip_id) REFERENCES equip_def(equip_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (node_id) REFERENCES node_def(node_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (host_id) REFERENCES host_def(host_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (param_no) REFERENCES equip_param_def(param_no) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE area_def (
	area_id			INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '空间序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	area_no			VARCHAR(10) NOT NULL COMMENT '空间编号',
	area_name		VARCHAR(50) COMMENT '空间名称',
	area_location	VARCHAR(50) COMMENT '所在位置',
	area_value		DOUBLE COMMENT '面积',
	area_hight		DOUBLE COMMENT '高度',
	memo			VARCHAR(255) COMMENT '备注说明',
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE equip_are_map (
	equip_id		INTEGER NOT NULL COMMENT '设备序号',
	area_id			INTEGER NOT NULL COMMENT '空间序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	PRIMARY KEY (equip_id, area_id),
	FOREIGN KEY (equip_id) REFERENCES equip_def(equip_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (area_id) REFERENCES area_def(area_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE schedule_def (
	sche_id			INTEGER AUTO_INCREMENT PRIMARY KEY COMMENT '计划序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	sche_no			VARCHAR(10) NOT NULL COMMENT '计划编号',
	sche_name		VARCHAR(50) COMMENT '计划名称',
	sche_type		CHAR(10) COMMENT '计划类型，TIMING定时，CYCLING循环，SENSOR采集，SCENERY场景',
	action			CHAR(10) COMMENT '执行动作',
	act_on_time		INTEGER COMMENT '动作持续时间，单位分钟',
	act_day			CHAR COMMENT '动作日',
	setup_day		DATETIME COMMENT '设置日',
	repeat_mode		CHAR(10) COMMENT '重复模式，ODD_DAY奇数日、EVEN_DAY偶数日、INT_DAY间隔日、WORKDAY工作日、WEEKEND周末、HOLIDAY节假日、MANUAL手动设置',
	int_act_day		BINARY COMMENT 'INT_DAY间隔日、MANUAL动作日',
	concurrent		INTEGER COMMENT '同时数量',
	cycle_day		INTEGER COMMENT '循环周期天数',
	cycle_num		INTEGER COMMENT '每天循环次数',
	start_num		INTEGER COMMENT '每天启动次数',
	condition_num	INTEGER COMMENT '采集条件个数',
	memo			VARCHAR(255) COMMENT '备注说明',
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE schedule_except_def (
	sche_id			INTEGER PRIMARY KEY COMMENT '计划序号',
	except_day		DATE NOT NULL COMMENT '例外日',
	execution		CHAR(1) DEFAULT 'Y' CHECK (execution IN ('Y', 'N')) COMMENT '执行',
	FOREIGN KEY (sche_id) REFERENCES schedule_def(sche_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE schedule_equip (
	sche_id			INTEGER NOT NULL COMMENT '计划序号',
	equip_id		INTEGER NOT NULL COMMENT '设备序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	execution_seq	INTEGER COMMENT '同一计划设备执行顺序',
	PRIMARY KEY (sche_id, equip_id),
	FOREIGN KEY (sche_id) REFERENCES schedule_def(sche_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (equip_id) REFERENCES equip_def(equip_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE schedule_history (
	sche_id			INTEGER NOT NULL COMMENT '计划序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	recv_time		DATETIME(6) COMMENT '接收时间',
	run_mode		CHAR(10) COMMENT '运行模式',
	PRIMARY KEY (recv_time, sche_id),
	FOREIGN KEY (sche_id) REFERENCES schedule_def(sche_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE schedule_start (
	sche_id			INTEGER NOT NULL COMMENT '计划序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	start_time		INTEGER COMMENT '启动时分',
	PRIMARY KEY (sche_id, start_time),
	FOREIGN KEY (sche_id) REFERENCES schedule_def(sche_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE schedule_condition (
	sche_id			INTEGER NOT NULL COMMENT '计划序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	cond_seq		INTEGER COMMENT '条件顺序号',
	high_act		CHAR(10) COMMENT '高于工作',
	high_value		DOUBLE COMMENT '高于数值',
	low_act			CHAR(10) COMMENT '低于动作',
	low_value		DOUBLE COMMENT '低于数值',
	PRIMARY KEY (sche_id, cond_seq),
	FOREIGN KEY (sche_id) REFERENCES schedule_def(sche_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE schedule_area_map (
	sche_id			INTEGER NOT NULL COMMENT '计划序号',
	area_id			INTEGER NOT NULL COMMENT '空间序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	PRIMARY KEY (sche_id, area_id),
	FOREIGN KEY (sche_id) REFERENCES schedule_def(sche_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (area_id) REFERENCES area_def(area_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE permition_equip_def (
	user_id			INTEGER NOT NULL COMMENT '人员编号',
	equip_id		INTEGER NOT NULL COMMENT '设备序号',
	area_id			INTEGER NOT NULL COMMENT '空间序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	setup_time		DATETIME COMMENT '设置时间',
	permition		CHAR(1) DEFAULT 'N' CHECK (permition IN ('R','V','N')) COMMENT '权限，R运行，V查看，N无权限',
	PRIMARY KEY (setup_time, user_id, equip_id, area_id),
	FOREIGN KEY (user_id) REFERENCES user_def(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (equip_id) REFERENCES equip_def(equip_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (area_id) REFERENCES area_def(area_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

CREATE TABLE permition_sche_def (
	user_id			INTEGER NOT NULL COMMENT '人员编号',
	sche_id			INTEGER NOT NULL COMMENT '计划序号',
	system_id		INTEGER NOT NULL COMMENT '系统序号',
	setup_time		DATETIME COMMENT '设置时间',
	permition		CHAR(1) DEFAULT 'N' CHECK (permition IN ('R','V','N')) COMMENT '权限，R运行，V查看，N无权限',
	PRIMARY KEY (setup_time, user_id, sche_id),
	FOREIGN KEY (user_id) REFERENCES user_def(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (sche_id) REFERENCES schedule_def(sche_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (system_id) REFERENCES system_def(system_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;


-- below architecture in memory
-- connection information
CREATE TABLE mem_web_conn (
	user_id			INTEGER PRIMARY KEY COMMENT '人员序号',
	system_id		INTEGER COMMENT '系统序号',
	token			CHAR(129) COMMENT '系统赋予令牌',
	connection		VARCHAR(10)	COMMENT '连接来源WEB，wechart，dingding',
	conn_time		DATETIME(6) COMMENT '连接时间',
	last_check		DATETIME(6) COMMENT '最近心跳包',
	status			CHAR(10) COMMENT '当前状态，ACTIVE、INACTIVE'
) ENGINE = MEMORY;

CREATE TABLE mem_lora_conn (
	dev_eui			CHAR(65) PRIMARY KEY COMMENT '设备唯一号',
	conn_time		DATETIME(6) COMMENT '连接时间',
	last_check		DATETIME(6) COMMENT '最近一次接收',
	status			CHAR(10) COMMENT '当前状态，ACTIVE、INACTIVE'
) ENGINE = MEMORY;

CREATE TABLE mem_host_conn (
	host_id			INTEGER PRIMARY KEY COMMENT '主机序号',
	system_id		INTEGER COMMENT '系统序号',
	token			CHAR(129) COMMENT '系统赋予令牌',
	conn_time		DATETIME(6) COMMENT '连接时间',
	last_check		DATETIME(6) COMMENT '最近一次接收',
	status			CHAR(10) COMMENT '当前状态，ACTIVE、INACTIVE'
) ENGINE = MEMORY;

-- bolow cache buffer
-- loraWAN mqtt
CREATE TABLE mem_mqtt_subscribe_lora (
	serial_no		INTEGER AUTO_INCREMENT PRIMARY KEY,
	dev_eui			CHAR(65) COMMENT '设备唯一号',
	need_answer		CHAR(1) COMMENT "要求回复，'Y'、'N' ",
	protocal		CHAR(10) COMMENT '协议类型，DOL、MODBU、JNAPI',
	dev_type		CHAR(10) COMMENT '设备类型，空调、电测、开关、烟感',
	rssi			INTEGER COMMENT '信号强度',
	snr				DOUBLE COMMENT '信噪比',
	recv_data		JSON COMMENT '接收数据',
	recv_time		DATETIME(6)COMMENT '接收时间',
	len_data		INTEGER COMMENT '数据长度',
	process_status	CHAR(4) DEFAULT 'NEW' CHECK (process_status IN ('NEW', 'PRC', 'SYN')) COMMENT '数据处理过程状态 New Process Saved'
) ENGINE = InnoDB;

CREATE TABLE mem_mqtt_publish_lora ( -- schedule action / setup instruct
	serial_no		INTEGER AUTO_INCREMENT PRIMARY KEY,
	dev_eui			CHAR(65) COMMENT '设备唯一号',
	need_answer		CHAR(1) COMMENT "要求回复，'Y'、'N'",
	protocal		CHAR(10) COMMENT '协议类型，DOL、MODBU、JNAPI',
	dev_type		CHAR(10) COMMENT '设备类型，空调、电测、开关、烟感',
	send_data		JSON COMMENT '发送数据, ACT 或者 SETUP',		
	len_data		INTEGER COMMENT '数据长度',
	send_time		DATETIME(6) COMMENT '发送时间',
	time_delay		INTEGER	COMMENT "检测延时，当need_answer='Y'时",
	remain_time		INTEGER COMMENT '检测超时，当send_data发出后，remain_time=time_delay，当remain_time=0时，重新发送这条send_data'
) ENGINE = InnoDB;

-- web socket 
CREATE TABLE mem_web_socket_receipt (
	serial_no		INTEGER AUTO_INCREMENT PRIMARY KEY,
	user_id			INTEGER COMMENT '用户序号',
	system_id		INTEGER COMMENT '系统序号',
	recv_time		DATETIME(6) DEFAULT CURRENT_TIMESTEMP COMMENT '接收时间',
	recv_data		JSON COMMENT '接收数据',
	need_answer		CHAR(1) DEFAULT 'Y' CHECK (need_answer IN ('Y', 'N')) COMMENT '要求回复',
	process_status	CHAR(4) DEFAULT 'NEW' CHECK (process_status IN ('NEW', 'PRC', 'SYN')) COMMENT '数据处理过程状态 New Process Saved'
) ENGINE = InnoDB;

CREATE TABLE mem_web_socket_transit (
	serial_no		INTEGER AUTO_INCREMENT PRIMARY KEY,
	user_id			INTEGER COMMENT '用户序号',
	system_id		INTEGER COMMENT '系统序号',
	send_time		DATETIME(6) COMMENT '发送时间',
	send_data		JSON COMMENT '发送数据'
) ENGINE = InnoDB;

-- host mqtt
CREATE TABLE mem_cloud_receipt (
	serial_no		INTEGER AUTO_INCREMENT PRIMARY KEY,
	host_id			INTEGER COMMENT '主机序号',
	recv_time		DATETIME(6) COMMENT '接收时间',
	recv_data		JSON COMMENT '接收数据',
	len_data		INTEGER COMMENT '数据长度',
	need_answer		CHAR(1) DEFAULT 'Y' CHECK (need_answer IN ('Y', 'N')) COMMENT '要求回复',
	process_status	CHAR(4) DEFAULT 'NEW' CHECK (process_status IN ('NEW', 'PRC', 'SYN')) COMMENT '数据处理过程状态 New Process Saved'
) ENGINE = InnoDB;

CREATE TABLE mem_cloud_transit ( -- 所有发出都要求回复
	serial_no		INTEGER AUTO_INCREMENT PRIMARY KEY,
	host_id			INTEGER COMMENT '主机序号',
	need_answer		CHAR(1) DEFAULT 'Y' CHECK (need_answer IN ('Y', 'N')) COMMENT '要求回复',
	send_data		JSON COMMENT '发送数据',
	len_data		INTEGER COMMENT '数据长度',
	send_time		DATETIME(6) COMMENT '发送时间',
	time_delay		INTEGER	COMMENT '检测延时',
	remain_time		INTEGER COMMENT '检测超时，当send_data发出后，remain_time=time_delay，当remain_time=0时，重新发送这条send_data'
) ENGINE = InnoDB;

-- schedule process
CREATE TABLE mem_schedule_list (
	sche_id			INTEGER PRIMARY KEY COMMENT '计划序号',
	time_delay		INTEGER	COMMENT '检测延时',
	remain_time		INTEGER COMMENT '检测超时',
	process_status	CHAR(1) COMMENT '数据处理过程状态'
) ENGINE = MEMORY;

CREATE TABLE mem_schedule_action (
	sche_id			INTEGER COMMENT '计划序号',
	equip_id		INTEGER COMMENT '设备序号',
	action			CHAR(10) COMMENT '执行动作',
	act_on_time		INTEGER	COMMENT '动作持续时间',
	remain_time		INTEGER COMMENT '检测超时',
	process_status	CHAR(1) COMMENT '数据处理过程状态',
	PRIMARY KEY (remain_time, sche_id, equip_id)
) ENGINE = MEMORY;

-- data query from web socket
CREATE TABLE mem_query_requst (
	user_id			INTEGER PRIMARY KEY COMMENT '用户序号',
	system_id		INTEGER COMMENT '系统序号',
	query_requsest	JSON COMMENT '查询请求'
) ENGINE = InnoDB;

-- data sync
CREATE TABLE mem_need_sync (
	buffer_id		CHAR(10) COMMENT '',
	recv_time		DATETIME(6) COMMENT '接收时间',
	sync_data		JSON COMMENT '需要同步数据',
	PRIMARY KEY (recv_time, buffer_id)
) ENGINE = InnoDB;

