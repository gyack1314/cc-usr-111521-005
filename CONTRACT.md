# 业务资料约定

fund 的 holding.weight 是母基金净资产中的价值比例，所有已知权重之和不能超过 1；缺额属于 undisclosed，不假定为现金。cash 必须显式记录。holding.target 可以是 fund、security 或 cash。直接头寸 amount 为本币市值，fx 为指定 valuation_day 的每单位本币折算基准币金额。security 指向 issuer 与 instrument，权益归属排放使用 equity_value 分母，若只有 enterprise_value 不能擅自替代；普通债的排放归属按该 instrument 声明的 denominator_kind 确定。issuer.emissions 为企业总排放，不是单证券排放。scenario 的 shock 为证券市值变化比例。循环持有的权重方程可无唯一解；未披露残余与闭环无法识别部分应保留独立质量。
