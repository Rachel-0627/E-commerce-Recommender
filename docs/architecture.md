# MVP 架构设计

## 总体流程

```text
前端方向推荐页
  -> Direction Recommendation API
  -> 用户画像 / 当前倾向 / 预算 / 资源
  -> Direction Recommendation Service
  -> 返回方向建议
  -> 进入商品推荐页
  -> Recommendation API
  -> User Profile / Product Catalog
  -> Recommendation Service
  -> Explanation Service
  -> 返回商品 + 推荐标签 + 推荐解释
```

## 模块说明

### API 层

提供对外接口：

- `GET /health`
- `GET /api/llm/status`
- `GET /api/users/{user_id}`
- `GET /api/users`
- `POST /api/users`
- `PATCH /api/users/{user_id}`
- `GET /api/directions`
- `GET /api/directions/{direction_id}`
- `POST /api/directions`
- `PATCH /api/directions/{direction_id}`
- `GET /api/directions/{direction_id}/products`
- `PUT /api/directions/{direction_id}/products`
- `GET /api/products`
- `GET /api/products/{product_id}`
- `POST /api/products`
- `PATCH /api/products/{product_id}`
- `POST /api/direction-recommendations`
- `GET /api/recommendations`
- `POST /api/events`
- `GET /api/events/summary`
- `POST /api/explanation-feedback`
- `GET /api/analytics/summary`

### 用户画像模块

第一阶段使用模拟数据，后续迁移到数据库。

画像字段：

- 长期兴趣
- 近期兴趣
- 品牌偏好
- 价格区间
- 负向偏好

### 商品模块

第一阶段使用内存商品数据。

商品字段：

- 商品 ID
- 标题
- 类目
- 品牌
- 价格
- 特征标签
- 评分
- 库存
- 图片地址

商品详情页会读取完整商品信息，并在用户点击、浏览、收藏、加购、不感兴趣时写入行为日志。

### 推荐模块

MVP 使用 ItemCF 协同过滤 + 用户画像规则 + 趋势热度：

```text
种子行为数据 data/events.json
+ 前端实时行为埋点
 + product_trends 趋势数据
 + product_sync_sources 自动同步商品来源
-> 构建用户-商品行为矩阵
-> 计算商品相似度
-> 生成 ItemCF 推荐分
-> 融合用户画像规则分
-> 融合 trend_score
-> 返回推荐商品和解释
```

行为权重：

```text
view: 1
click: 2
favorite: 3
add_to_cart: 4
purchase: 5
dislike: -3
```

推荐来源：

```text
itemcf: 基于相似用户行为的推荐
profile_rule: 用户画像和商品规则兜底推荐
```

趋势数据当前保存在 SQLite 的 `product_trends` 表，既可以通过脚本从 `data/product_trends.json` 导入，也可以通过 API 增量写入。

商品资源现在除了手工导入和批量导入外，还支持“可重复执行的同步来源”。同步来源保存在 SQLite 的 `product_sync_sources` 表，可以指向本地文件或远程 URL，并通过统一的同步服务把商品再次导入到 `products` 表。

后续增强为：

```text
+ 文本向量召回
+ LightGBM 排序
+ LLM 解释
```

### 解释模块

当前使用结构化标签 + 可选 LLM 解释 + 模板兜底。

默认解释链路：

```text
reason_tags
  -> 模板解释
```

启用 `LLM_PROVIDER=openai` 且配置 `OPENAI_API_KEY` 和 `OPENAI_MODEL` 后：

```text
reason_tags
  -> 用户画像和商品证据
  -> Prompt
  -> OpenAI Responses API
  -> 安全校验
  -> LLM 解释
```

如果 LLM 未配置、调用失败或输出未通过安全校验，系统自动回退到模板解释。

后续增强为：

```text
reason_tags
  -> evidence
  -> RAG 商品知识检索
  -> LLM 生成
  -> 安全校验
```

## 推荐接口返回结构

```json
{
  "request_id": "req_xxx",
  "user_id": "u_001",
  "scene": "home",
  "items": [
    {
      "product_id": "p_001",
      "title": "轻量缓震跑鞋",
      "score": 0.92,
      "reason_tags": ["近期兴趣相关", "价格区间匹配"],
      "explanation": "根据你近期关注的跑步装备，这款商品在价格和功能上比较符合你的偏好。"
    }
  ]
}
```

## 运行时效果统计

第五阶段新增运行时推荐日志和轻量统计接口。当前运行时数据已经持久化到 SQLite。

每次推荐请求会记录：

```text
request_id
user_id
product_id
rank
score
scene
recommendation_source
reason_tags
explanation
```

统计指标包括：

```text
推荐请求数
商品曝光数
点击数
CTR
加购次数
加购率
解释反馈数
解释有用率
Top 商品表现
```

当前本地数据库：

```text
data/app.sqlite3
```

持久化表：

```text
users
products
user_events
recommendation_logs
explanation_feedback
```

服务重启后，用户画像、商品主数据、推荐日志、行为日志和解释反馈仍然保留。后续可迁移到 PostgreSQL。

启动时如果用户表和商品表为空，系统会从 `backend/app/sample_data.py` 导入初始用户和商品。

用户和商品支持通过 API 管理：

```text
POST /api/users 创建或覆盖用户画像
PATCH /api/users/{user_id} 局部更新用户画像
POST /api/products 创建或覆盖商品
PATCH /api/products/{product_id} 局部更新商品
```

方向推荐模块已接入：

```text
directions
direction_products
```

支持两种推荐方式：

```text
模式 A：没有明确方向
-> 传兴趣、倾向品类、预算、已有资源
-> 返回推荐方向

模式 B：已有用户画像
-> 传 user_id
-> 返回与用户情况更匹配的方向
```

方向推荐返回：

```text
方向标题
品类
预算范围
难度
推荐理由
starter_products
```

当用户选中某个方向后，前端会把该方向的 `direction_id` 带入商品推荐接口，形成：

```text
方向推荐
  -> 选定 direction_id
  -> GET /api/recommendations?direction_id=...
  -> 返回该方向下的具体商品
```
