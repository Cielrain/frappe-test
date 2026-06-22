from random import Random

import frappe
from frappe.utils import add_days, add_months, getdate


ACCOUNTS = [
    ("ZE-1001", "杭州滨江骑手-李明", "Rider", "Hangzhou Core", "杭州", "Food Delivery", "Station Walk-in", "Rider Unlimited", "星耀城换电站"),
    ("ZE-1002", "顺丰同城杭州西湖站", "Fleet Customer", "Hangzhou Core", "杭州", "Express Delivery", "Fleet Contract", "Fleet Premium", "古荡换电站"),
    ("ZE-1003", "美团骑手-王凯", "Rider", "Ningbo Network", "宁波", "Food Delivery", "Rider Referral", "Rider Monthly", "天一广场换电站"),
    ("ZE-1004", "义乌小商品城配送队", "Fleet Customer", "Jinhua-Yiwu", "义乌", "City Distribution", "Platform Cooperation", "Fleet Standard", "国际商贸城换电站"),
    ("ZE-1005", "绍兴柯桥加盟站", "Franchise Station", "Shaoxing-Huzhou", "绍兴", "Station Operation", "Local Operator", "Station Operation", "柯桥轻纺城站"),
    ("ZE-1006", "宁波北仑港区配送队", "Fleet Customer", "Ningbo Network", "宁波", "City Distribution", "Fleet Contract", "Fleet Premium", "北仑港换电站"),
    ("ZE-1007", "上海松江即时零售队", "Fleet Customer", "Shanghai Periphery", "上海", "Instant Retail", "Platform Cooperation", "Fleet Standard", "松江大学城换电站"),
    ("ZE-1008", "湖州织里骑手-陈越", "Rider", "Shaoxing-Huzhou", "湖州", "Express Delivery", "Operations Campaign", "Rider Monthly", "织里童装城站"),
    ("ZE-1009", "杭州下沙校园服务队", "Fleet Customer", "Hangzhou Core", "杭州", "Campus Service", "Device Sales", "Fleet Standard", "下沙高教园站"),
    ("ZE-1010", "金华婺城骑手-周航", "Rider", "Jinhua-Yiwu", "金华", "Food Delivery", "Rider Referral", "Rider Monthly", "婺城万达换电站"),
    ("ZE-1011", "温州鹿城外卖联盟", "Fleet Customer", "Wenzhou Network", "温州", "Food Delivery", "Fleet Contract", "Fleet Premium", "鹿城五马街站"),
    ("ZE-1012", "杭州萧山直营站", "Direct Station", "Hangzhou Core", "杭州", "Station Operation", "Device Sales", "Station Operation", "萧山机场路站"),
    ("ZE-1013", "宁波鄞州骑手-赵磊", "Rider", "Ningbo Network", "宁波", "Instant Retail", "Station Walk-in", "Rider Unlimited", "鄞州万达换电站"),
    ("ZE-1014", "苏州园区配送队", "Fleet Customer", "Jiangsu Network", "苏州", "Express Delivery", "Platform Cooperation", "Fleet Standard", "金鸡湖换电站"),
    ("ZE-1015", "义乌北苑加盟站", "Franchise Station", "Jinhua-Yiwu", "义乌", "Station Operation", "Local Operator", "Station Operation", "北苑快递园站"),
    ("ZE-1016", "嘉兴南湖骑手-刘一", "Rider", "Shaoxing-Huzhou", "嘉兴", "Food Delivery", "Operations Campaign", "Rider Monthly", "南湖万达站"),
    ("ZE-1017", "温州龙湾同城配送", "Fleet Customer", "Wenzhou Network", "温州", "City Distribution", "Fleet Contract", "Fleet Standard", "龙湾机场站"),
    ("ZE-1018", "上海青浦快递站", "Fleet Customer", "Shanghai Periphery", "上海", "Express Delivery", "Fleet Contract", "Fleet Premium", "青浦奥莱站"),
    ("ZE-1019", "杭州余杭骑手-孙杰", "Rider", "Hangzhou Core", "杭州", "Instant Retail", "Station Walk-in", "Rider Unlimited", "未来科技城站"),
    ("ZE-1020", "绍兴越城校园服务", "Fleet Customer", "Shaoxing-Huzhou", "绍兴", "Campus Service", "Platform Cooperation", "Fleet Standard", "越城大学城站"),
    ("ZE-1021", "宁波慈溪直营站", "Direct Station", "Ningbo Network", "慈溪", "Station Operation", "Device Sales", "Station Operation", "慈溪银泰站"),
    ("ZE-1022", "金华永康五金配送", "Fleet Customer", "Jinhua-Yiwu", "永康", "City Distribution", "Fleet Contract", "Fleet Standard", "永康总部中心站"),
    ("ZE-1023", "杭州上城骑手-阿森", "Rider", "Hangzhou Core", "杭州", "Food Delivery", "Rider Referral", "Rider Monthly", "湖滨银泰换电站"),
    ("ZE-1024", "苏州昆山即时零售", "Fleet Customer", "Jiangsu Network", "昆山", "Instant Retail", "Platform Cooperation", "Fleet Premium", "昆山花桥站"),
]


PLAN_REVENUE = {
    "Trial": 0,
    "Rider Monthly": 299,
    "Rider Unlimited": 499,
    "Fleet Standard": 3800,
    "Fleet Premium": 9800,
    "Station Operation": 16800,
}

PLAN_QUOTA = {
    "Trial": 20,
    "Rider Monthly": 90,
    "Rider Unlimited": 180,
    "Fleet Standard": 1200,
    "Fleet Premium": 3600,
    "Station Operation": 12000,
}


def after_install():
    seed_mock_data()


def seed_mock_data():
    if frappe.db.exists("Energy Service Lifecycle Event", {"customer_id": ["like", "ZE-%"]}):
        return

    rng = Random(86)
    base_date = getdate("2025-07-01")
    churn_reasons = [
        "Station Too Far",
        "Battery Availability",
        "Price Sensitivity",
        "Vehicle Retired",
        "Fleet Contract Ended",
        "Competitor Station",
    ]

    for index, account in enumerate(ACCOUNTS):
        account_id, account_name, object_type, region, city, scenario, channel, plan, station = account
        start_date = add_days(add_months(base_date, index % 10), rng.randint(0, 20))
        revenue = PLAN_REVENUE[plan]
        quota = PLAN_QUOTA[plan]
        vehicle_type = _vehicle_for_scenario(scenario, object_type)
        battery_model = _battery_for_vehicle(vehicle_type)

        _insert_event(
            customer_id=account_id,
            customer_name=account_name,
            service_object_type=object_type,
            event_type="Signup",
            event_date=start_date,
            service_plan=plan,
            mrr=revenue,
            monthly_swap_quota=quota,
            vehicle_type=vehicle_type,
            battery_model=battery_model,
            station_name=station,
            cabinet_count=_cabinet_count(object_type, plan),
            region=region,
            city=city,
            industry=scenario,
            channel=channel,
            health_score=rng.randint(68, 94),
            notes="Mock signup generated for Zhige battery swapping operations.",
        )

        if index % 3 != 0:
            _insert_event(
                customer_id=account_id,
                customer_name=account_name,
                service_object_type=object_type,
                event_type="Activation",
                event_date=add_days(start_date, rng.randint(3, 18)),
                service_plan=plan,
                mrr=revenue,
                monthly_swap_quota=quota,
                vehicle_type=vehicle_type,
                battery_model=battery_model,
                station_name=station,
                cabinet_count=_cabinet_count(object_type, plan),
                region=region,
                city=city,
                industry=scenario,
                channel=channel,
                health_score=rng.randint(76, 98),
                notes="First battery swap and service onboarding completed.",
            )

        if index % 4 == 1:
            expansion_revenue = int(revenue * rng.choice([0.25, 0.35, 0.5]))
            _insert_event(
                customer_id=account_id,
                customer_name=account_name,
                service_object_type=object_type,
                event_type="Expansion",
                event_date=add_days(add_months(start_date, rng.randint(2, 5)), rng.randint(0, 12)),
                service_plan=plan,
                mrr=expansion_revenue,
                monthly_swap_quota=int(quota * 0.35),
                vehicle_type=vehicle_type,
                battery_model=battery_model,
                station_name=station,
                cabinet_count=max(0, int(_cabinet_count(object_type, plan) * 0.35)),
                region=region,
                city=city,
                industry=scenario,
                channel=channel,
                health_score=rng.randint(82, 99),
                notes="Additional riders, cabinets, or monthly swap quota added.",
            )

        if index in {4, 9, 13, 18, 22}:
            _insert_event(
                customer_id=account_id,
                customer_name=account_name,
                service_object_type=object_type,
                event_type="Churn",
                event_date=add_days(add_months(start_date, rng.randint(3, 8)), rng.randint(4, 24)),
                service_plan=plan,
                mrr=revenue,
                monthly_swap_quota=quota,
                vehicle_type=vehicle_type,
                battery_model=battery_model,
                station_name=station,
                cabinet_count=_cabinet_count(object_type, plan),
                region=region,
                city=city,
                industry=scenario,
                channel=channel,
                health_score=rng.randint(18, 46),
                churn_reason=rng.choice(churn_reasons),
                notes="Mock churn event for operations analysis.",
            )

        if index in {9, 18}:
            _insert_event(
                customer_id=account_id,
                customer_name=account_name,
                service_object_type=object_type,
                event_type="Reactivation",
                event_date=add_days(add_months(start_date, 10), rng.randint(1, 18)),
                service_plan=plan,
                mrr=revenue,
                monthly_swap_quota=quota,
                vehicle_type=vehicle_type,
                battery_model=battery_model,
                station_name=station,
                cabinet_count=_cabinet_count(object_type, plan),
                region=region,
                city=city,
                industry=scenario,
                channel=channel,
                health_score=rng.randint(72, 90),
                notes="Recovered through station coverage and operations follow-up.",
            )

    frappe.db.commit()


def _vehicle_for_scenario(scenario, object_type):
    if object_type in {"Franchise Station", "Direct Station"}:
        return "Station Asset"
    if scenario in {"City Distribution", "Express Delivery"}:
        return "Cargo Tricycle"
    if scenario == "Food Delivery":
        return "Delivery Scooter"
    return "E-bike"


def _battery_for_vehicle(vehicle_type):
    if vehicle_type == "Cargo Tricycle":
        return "72V45Ah LFP"
    if vehicle_type == "Delivery Scooter":
        return "60V30Ah LFP"
    if vehicle_type == "Station Asset":
        return "Swapping Cabinet"
    return "48V24Ah LFP"


def _cabinet_count(object_type, plan):
    if object_type == "Direct Station":
        return 8
    if object_type == "Franchise Station":
        return 5
    if plan == "Fleet Premium":
        return 3
    if plan == "Fleet Standard":
        return 1
    return 0


def _insert_event(**values):
    doc = frappe.new_doc("Energy Service Lifecycle Event")
    doc.update(values)
    doc.insert(ignore_permissions=True)
