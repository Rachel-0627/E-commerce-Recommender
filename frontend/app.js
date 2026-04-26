const API_BASE_URL = "http://127.0.0.1:8000";

const userView = document.querySelector("#user-view");
const adminView = document.querySelector("#admin-view");
const navTabUser = document.querySelector("#nav-tab-user");
const navTabAdmin = document.querySelector("#nav-tab-admin");
const headerUserSelect = document.querySelector("#header-user-select");

const form = document.querySelector("#recommendation-form");
const userSelect = document.querySelector("#user-select");
const sceneSelect = document.querySelector("#scene-select");
const directionStage = document.querySelector("#direction-stage");
const productStage = document.querySelector("#product-stage");
const enterGeneralProductsButton = document.querySelector("#enter-general-products");
const backToDirectionsButton = document.querySelector("#back-to-directions");
const productStageTitle = document.querySelector("#product-stage-title");
const productStageIntro = document.querySelector("#product-stage-intro");
const activeDirectionBanner = document.querySelector("#active-direction-banner");
const activeDirectionText = document.querySelector("#active-direction-text");
const clearDirectionFilterButton = document.querySelector("#clear-direction-filter");
const directionLayerPanel = document.querySelector("#direction-layer-panel");
const directionLayerStatus = document.querySelector("#direction-layer-status");
const directionLayerGrid = document.querySelector("#direction-layer-grid");
const directionUserForm = document.querySelector("#direction-user-form");
const directionCategoryForm = document.querySelector("#direction-category-form");
const directionGrid = document.querySelector("#direction-grid");
const directionStatus = document.querySelector("#direction-status");
const directionTemplate = document.querySelector("#direction-card-template");
const directionBudgetInput = document.querySelector("#direction-budget");
const directionInterestsInput = document.querySelector("#direction-interests");
const directionResourcesInput = document.querySelector("#direction-resources");
const directionCategorySelect = document.querySelector("#direction-category");
const directionCategoryBudgetInput = document.querySelector("#direction-category-budget");
const directionCategoryInterestsInput = document.querySelector("#direction-category-interests");
const directionModeButtons = document.querySelectorAll("[data-direction-mode]");
const grid = document.querySelector("#recommendation-grid");
const statusText = document.querySelector("#status-text");
const requestIdText = document.querySelector("#request-id");
const template = document.querySelector("#product-card-template");
const metricTemplate = document.querySelector("#metric-card-template");
const topProductTemplate = document.querySelector("#top-product-template");
const trendRowTemplate = document.querySelector("#trend-row-template");
const metricGrid = document.querySelector("#metric-grid");
const topProductList = document.querySelector("#top-product-list");
const refreshAnalyticsButton = document.querySelector("#refresh-analytics");
const refreshTrendsButton = document.querySelector("#refresh-trends");
const trendFilterForm = document.querySelector("#trend-filter-form");
const trendSourceFilter = document.querySelector("#trend-source-filter");
const trendCategoryFilter = document.querySelector("#trend-category-filter");
const trendCreateForm = document.querySelector("#trend-create-form");
const trendCreateSourceInput = document.querySelector("#trend-create-source");
const trendCreateKeywordInput = document.querySelector("#trend-create-keyword");
const trendCreateCategoryInput = document.querySelector("#trend-create-category");
const trendCreateScoreInput = document.querySelector("#trend-create-score");
const trendCreateSalesScoreInput = document.querySelector("#trend-create-sales-score");
const trendCreateProductSelect = document.querySelector("#trend-create-product");
const trendCreateStatus = document.querySelector("#trend-create-status");
const trendImportForm = document.querySelector("#trend-import-form");
const trendImportAdapterSelect = document.querySelector("#trend-import-adapter");
const trendImportFileInput = document.querySelector("#trend-import-file");
const trendImportContentInput = document.querySelector("#trend-import-content");
const trendImportStatus = document.querySelector("#trend-import-status");
const trendPreviewSubmitButton = document.querySelector("#trend-preview-submit");
const trendPreviewMetricGrid = document.querySelector("#trend-preview-metric-grid");
const trendPreviewList = document.querySelector("#trend-preview-list");
const trendPreviewStatus = document.querySelector("#trend-preview-status");
const trendPresetPanel = document.querySelector("#trend-preset-panel");
const trendStatus = document.querySelector("#trend-status");
const trendMetricGrid = document.querySelector("#trend-metric-grid");
const trendList = document.querySelector("#trend-list");
const refreshProductSourcesButton = document.querySelector("#refresh-product-sources");
const productSourceFilterForm = document.querySelector("#product-source-filter-form");
const productSourceFilter = document.querySelector("#product-source-filter");
const productCategoryFilter = document.querySelector("#product-category-filter");
const productSourceStatus = document.querySelector("#product-source-status");
const productSourceMetricGrid = document.querySelector("#product-source-metric-grid");
const productImportForm = document.querySelector("#product-import-form");
const productImportAdapterSelect = document.querySelector("#product-import-adapter");
const productImportFileInput = document.querySelector("#product-import-file");
const productImportContentInput = document.querySelector("#product-import-content");
const productImportStatus = document.querySelector("#product-import-status");
const productPreviewSubmitButton = document.querySelector("#product-preview-submit");
const productPreviewMetricGrid = document.querySelector("#product-preview-metric-grid");
const productPreviewList = document.querySelector("#product-preview-list");
const productPreviewStatus = document.querySelector("#product-preview-status");
const productPresetPanel = document.querySelector("#product-preset-panel");
const productSourceList = document.querySelector("#product-source-list");
const productSourceRowTemplate = document.querySelector("#product-source-row-template");
const productPreviewRowTemplate = document.querySelector("#product-preview-row-template");
const refreshProductSyncButton = document.querySelector("#refresh-product-sync");
const runAllProductSyncButton = document.querySelector("#run-all-product-sync");
const productSyncFilterForm = document.querySelector("#product-sync-filter-form");
const productSyncTypeFilter = document.querySelector("#product-sync-type-filter");
const productSyncEnabledFilter = document.querySelector("#product-sync-enabled-filter");
const productSyncCreateForm = document.querySelector("#product-sync-create-form");
const productSyncCreateIdInput = document.querySelector("#product-sync-create-id");
const productSyncCreateNameInput = document.querySelector("#product-sync-create-name");
const productSyncCreateTypeInput = document.querySelector("#product-sync-create-type");
const productSyncCreateLocationInput = document.querySelector("#product-sync-create-location");
const productSyncCreateAdapterSelect = document.querySelector("#product-sync-create-adapter");
const productSyncCreateEnabledSelect = document.querySelector("#product-sync-create-enabled");
const productSyncCreateNotesInput = document.querySelector("#product-sync-create-notes");
const productSyncStatus = document.querySelector("#product-sync-status");
const productSyncMetricGrid = document.querySelector("#product-sync-metric-grid");
const productSyncList = document.querySelector("#product-sync-list");
const productSyncRowTemplate = document.querySelector("#product-sync-row-template");
const refreshProductManagementButton = document.querySelector("#refresh-product-management");
const productManagementFilterForm = document.querySelector("#product-management-filter-form");
const productManagementSourceFilter = document.querySelector("#product-management-source-filter");
const productManagementCategoryFilter = document.querySelector("#product-management-category-filter");
const productCreateForm = document.querySelector("#product-create-form");
const productCreateIdInput = document.querySelector("#product-create-id");
const productCreateTitleInput = document.querySelector("#product-create-title");
const productCreateCategoryInput = document.querySelector("#product-create-category");
const productCreateBrandInput = document.querySelector("#product-create-brand");
const productCreatePriceInput = document.querySelector("#product-create-price");
const productCreateStockInput = document.querySelector("#product-create-stock");
const productCreateRatingInput = document.querySelector("#product-create-rating");
const productCreateSourceInput = document.querySelector("#product-create-source");
const productCreateExternalIdInput = document.querySelector("#product-create-external-id");
const productCreatePopularityInput = document.querySelector("#product-create-popularity");
const productCreateSalesInput = document.querySelector("#product-create-sales");
const productCreateImageInput = document.querySelector("#product-create-image");
const productCreateFeaturesInput = document.querySelector("#product-create-features");
const productCreateDescriptionInput = document.querySelector("#product-create-description");
const productManagementStatus = document.querySelector("#product-management-status");
const productManagementMetricGrid = document.querySelector("#product-management-metric-grid");
const productManagementList = document.querySelector("#product-management-list");
const productManagementRowTemplate = document.querySelector("#product-management-row-template");
const refreshUserManagementButton = document.querySelector("#refresh-user-management");
const userManagementFilterForm = document.querySelector("#user-management-filter-form");
const userBudgetFilter = document.querySelector("#user-budget-filter");
const userInterestFilter = document.querySelector("#user-interest-filter");
const userCreateForm = document.querySelector("#user-create-form");
const userCreateIdInput = document.querySelector("#user-create-id");
const userCreateNameInput = document.querySelector("#user-create-name");
const userCreatePriceMinInput = document.querySelector("#user-create-price-min");
const userCreatePriceMaxInput = document.querySelector("#user-create-price-max");
const userCreateLongInterestsInput = document.querySelector("#user-create-long-interests");
const userCreateRecentInterestsInput = document.querySelector("#user-create-recent-interests");
const userCreateBrandsInput = document.querySelector("#user-create-brands");
const userCreateNegativeTagsInput = document.querySelector("#user-create-negative-tags");
const userManagementStatus = document.querySelector("#user-management-status");
const userManagementMetricGrid = document.querySelector("#user-management-metric-grid");
const userManagementList = document.querySelector("#user-management-list");
const userManagementRowTemplate = document.querySelector("#user-management-row-template");
const refreshDirectionManagementButton = document.querySelector("#refresh-direction-management");
const directionManagementFilterForm = document.querySelector("#direction-management-filter-form");
const directionManagementCategoryFilter = document.querySelector("#direction-management-category-filter");
const directionManagementDifficultyFilter = document.querySelector("#direction-management-difficulty-filter");
const directionCreateForm = document.querySelector("#direction-create-form");
const directionCreateIdInput = document.querySelector("#direction-create-id");
const directionCreateTitleInput = document.querySelector("#direction-create-title");
const directionCreateCategoryInput = document.querySelector("#direction-create-category");
const directionCreateSceneInput = document.querySelector("#direction-create-scene");
const directionCreateDifficultyInput = document.querySelector("#direction-create-difficulty");
const directionCreateBudgetMinInput = document.querySelector("#direction-create-budget-min");
const directionCreateBudgetMaxInput = document.querySelector("#direction-create-budget-max");
const directionCreateInterestsInput = document.querySelector("#direction-create-interests");
const directionCreateProductSelector = document.querySelector("#direction-create-product-selector");

const DIRECTION_ROLES = ["核心商品", "入门款", "进阶款", "搭配款", "替代款", "推荐商品"];
const directionCreateDescriptionInput = document.querySelector("#direction-create-description");
const directionManagementStatus = document.querySelector("#direction-management-status");
const directionManagementMetricGrid = document.querySelector("#direction-management-metric-grid");
const directionManagementList = document.querySelector("#direction-management-list");
const directionManagementRowTemplate = document.querySelector("#direction-management-row-template");
const refreshImportHistoryButton = document.querySelector("#refresh-import-history");
const importHistoryFilterForm = document.querySelector("#import-history-filter-form");
const importEntityFilter = document.querySelector("#import-entity-filter");
const importOperationFilter = document.querySelector("#import-operation-filter");
const importHistoryStatus = document.querySelector("#import-history-status");
const importHistoryMetricGrid = document.querySelector("#import-history-metric-grid");
const importHistoryList = document.querySelector("#import-history-list");
const importHistoryRowTemplate = document.querySelector("#import-history-row-template");
const productDialog = document.querySelector("#product-dialog");
const dialogClose = document.querySelector("#dialog-close");
const detailEventStatus = document.querySelector("#detail-event-status");
const trendPreviewRowTemplate = document.querySelector("#trend-preview-row-template");

let latestRequestId = "";
let activeProductId = "";
let activeUserId = "";
let activeScene = "";
let activeDirectionMode = "user";
let selectedDirectionId = "";
let selectedDirectionTitle = "";
let trendRecords = [];
let productCatalog = [];
let trendAdapters = [];
let productSourceAdapters = [];
let importHistoryRecords = [];
let userProfiles = [];
let directionCatalog = [];
let directionProductLinks = [];
let productSyncSources = [];

async function withButtonLoading(btn, label, fn) {
  const original = btn.textContent;
  btn.disabled = true;
  btn.textContent = label;
  try {
    await fn();
  } finally {
    btn.disabled = false;
    btn.textContent = original;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || form.querySelector('[type="submit"]');
  withButtonLoading(btn, "获取中...", loadRecommendations);
});

enterGeneralProductsButton.addEventListener("click", () => {
  navigateToProductStage();
});

backToDirectionsButton.addEventListener("click", () => {
  navigateToDirectionStage();
});

clearDirectionFilterButton.addEventListener("click", () => {
  clearDirectionFilter();
});

directionUserForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || directionUserForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "获取中...", loadDirectionRecommendationsForUser);
});

directionCategoryForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || directionCategoryForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "获取中...", loadDirectionRecommendationsForCategory);
});

directionModeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setDirectionMode(button.dataset.directionMode);
  });
});

refreshAnalyticsButton.addEventListener("click", () => {
  loadAnalytics();
});

refreshTrendsButton.addEventListener("click", () => {
  loadTrendManagement();
});

refreshProductSourcesButton.addEventListener("click", () => {
  loadProductSourceManagement();
});

refreshProductSyncButton.addEventListener("click", () => {
  loadProductSyncManagement();
});

runAllProductSyncButton.addEventListener("click", (e) => {
  withButtonLoading(e.currentTarget, "同步中...", runAllProductSyncSources);
});

refreshProductManagementButton.addEventListener("click", () => {
  loadProductSourceManagement();
});

refreshUserManagementButton.addEventListener("click", () => {
  loadUserManagement();
});

refreshDirectionManagementButton.addEventListener("click", () => {
  loadDirectionManagement();
});

refreshImportHistoryButton.addEventListener("click", () => {
  loadImportHistory();
});

trendFilterForm.addEventListener("change", () => {
  renderTrendManagement();
});

productSourceFilterForm.addEventListener("change", () => {
  renderProductSourceManagement();
});

productSyncFilterForm.addEventListener("change", () => {
  renderProductSyncManagement();
});

productSyncCreateForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || productSyncCreateForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "新增中...", createProductSyncSource);
});

productManagementFilterForm.addEventListener("change", () => {
  renderProductManagement();
});

productCreateForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || productCreateForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "新增中...", createManagedProduct);
});

userManagementFilterForm.addEventListener("input", () => {
  renderUserManagement();
});

userCreateForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || userCreateForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "新增中...", createManagedUser);
});

directionManagementFilterForm.addEventListener("change", () => {
  renderDirectionManagement();
});

directionCreateForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || directionCreateForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "新增中...", createManagedDirection);
});

importHistoryFilterForm.addEventListener("change", () => {
  renderImportHistory();
});

trendCreateForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || trendCreateForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "新增中...", createTrendRecord);
});

trendImportForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || trendImportForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "导入中...", importTrendBatch);
});

trendPreviewSubmitButton.addEventListener("click", (e) => {
  withButtonLoading(e.currentTarget, "解析中...", previewTrendBatch);
});

productPreviewSubmitButton.addEventListener("click", (e) => {
  withButtonLoading(e.currentTarget, "解析中...", previewProductBatch);
});

productImportForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const btn = event.submitter || productImportForm.querySelector('[type="submit"]');
  withButtonLoading(btn, "导入中...", importProductBatch);
});

userSelect.addEventListener("change", () => {
  if (isProductRoute()) {
    loadRecommendations();
  } else if (activeDirectionMode === "user") {
    loadDirectionRecommendationsForUser();
  }
});

sceneSelect.addEventListener("change", () => {
  if (isProductRoute()) {
    loadRecommendations();
  }
});

dialogClose.addEventListener("click", () => {
  productDialog.close();
});

productDialog.addEventListener("click", (event) => {
  if (event.target === productDialog) {
    productDialog.close();
  }
});

document.querySelectorAll("[data-event]").forEach((button) => {
  button.addEventListener("click", () => {
    submitProductEvent(button.dataset.event);
  });
});

window.addEventListener("hashchange", () => {
  syncStageFromHash();
});

function setDirectionMode(mode, { autoLoad = true } = {}) {
  activeDirectionMode = mode;
  directionModeButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.directionMode === mode);
  });
  directionUserForm.classList.toggle("is-hidden", mode !== "user");
  directionCategoryForm.classList.toggle("is-hidden", mode !== "category");

  if (!autoLoad) {
    return;
  }

  if (mode === "user") {
    loadDirectionRecommendationsForUser();
  } else {
    loadDirectionRecommendationsForCategory();
  }
}

async function loadRecommendations() {
  const userId = userSelect.value;
  const scene = sceneSelect.value;

  setStatus("正在获取推荐...", false);
  requestIdText.textContent = "";
  grid.innerHTML = "";

  try {
    const url = buildRecommendationUrl(userId, scene, selectedDirectionId);
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`推荐服务返回 ${response.status}`);
    }

    const payload = await response.json();
    latestRequestId = payload.request_id;
    activeUserId = payload.user_id;
    activeScene = payload.scene;
    renderRecommendations(payload);
    loadAnalytics();
  } catch (error) {
    setStatus(`无法连接推荐服务：${error.message}`, true);
    requestIdText.textContent = "请确认后端运行在 http://127.0.0.1:8000";
  }
}

function buildRecommendationUrl(userId, scene, directionId) {
  const params = new URLSearchParams({
    user_id: userId,
    scene,
    limit: "6",
  });

  if (directionId) {
    params.set("direction_id", directionId);
  }

  return `${API_BASE_URL}/api/recommendations?${params.toString()}`;
}

function renderRecommendations(payload) {
  if (!payload.items.length) {
    setStatus("暂无推荐结果", false);
    return;
  }

  setStatus(`已为 ${payload.user_id} 生成 ${payload.items.length} 条推荐`, false);
  if (selectedDirectionId && selectedDirectionTitle) {
    setStatus(`已在“${selectedDirectionTitle}”方向下生成 ${payload.items.length} 条商品推荐`, false);
  }
  requestIdText.textContent = `Request ID: ${payload.request_id}`;

  payload.items.forEach((item) => {
    const card = template.content.firstElementChild.cloneNode(true);
    const image = card.querySelector(".product-image");
    const detailButton = card.querySelector(".detail-button");
    const explanationData = {
      text: item.explanation,
      tags: item.reason_tags,
      provider: item.explanation_provider,
    };

    image.src = item.image_url;
    image.alt = item.title;
    card.dataset.productId = item.product_id;
    card.querySelector(".category").textContent = item.category;
    card.querySelector(".source-badge").textContent = sourceLabel(item.recommendation_source);
    card.querySelector(".product-title").textContent = item.title;
    card.querySelector(".brand-price").textContent = `${item.brand} · ¥${item.price}`;
    card.querySelector(".explanation").textContent = item.explanation;

    const tagList = card.querySelector(".tag-list");
    item.reason_tags.slice(0, 2).forEach((tag) => {
      const tagNode = document.createElement("span");
      tagNode.className = "tag";
      tagNode.textContent = tag;
      tagList.appendChild(tagNode);
    });

    const openDetail = () => openProductDetail(payload.user_id, item.product_id, payload.scene, explanationData);

    card.addEventListener("click", (event) => {
      if (event.target.closest("button")) return;
      openDetail();
    });

    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.target.closest("button")) openDetail();
    });

    detailButton.addEventListener("click", openDetail);

    grid.appendChild(card);
  });
}

async function loadDirectionRecommendationsForUser() {
  directionStatus.textContent = "正在获取方向推荐...";

  try {
    const payload = await postDirectionRecommendations({
      user_id: userSelect.value,
      interests: parseListInput(directionInterestsInput.value),
      existing_resources: parseListInput(directionResourcesInput.value),
      budget: parseNumberInput(directionBudgetInput.value),
      limit: 3,
    });
    renderDirectionRecommendations(payload);
  } catch (error) {
    directionGrid.innerHTML = "";
    directionStatus.textContent = `无法加载方向推荐：${error.message}`;
  }
}

async function loadDirectionRecommendationsForCategory() {
  directionStatus.textContent = "正在获取方向推荐...";

  try {
    const payload = await postDirectionRecommendations({
      preferred_categories: [directionCategorySelect.value],
      interests: parseListInput(directionCategoryInterestsInput.value),
      budget: parseNumberInput(directionCategoryBudgetInput.value),
      existing_resources: [],
      limit: 3,
    });
    renderDirectionRecommendations(payload);
  } catch (error) {
    directionGrid.innerHTML = "";
    directionStatus.textContent = `无法加载方向推荐：${error.message}`;
  }
}

async function postDirectionRecommendations(payload) {
  const response = await fetch(`${API_BASE_URL}/api/direction-recommendations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`方向推荐服务返回 ${response.status}`);
  }

  return response.json();
}

function renderDirectionRecommendations(payload) {
  directionGrid.innerHTML = "";

  if (!payload.items.length) {
    directionStatus.textContent = "暂无方向推荐结果";
    return;
  }

  directionStatus.textContent = payload.user_id
    ? `已基于 ${payload.user_id} 的画像生成 ${payload.items.length} 个方向`
    : `已生成 ${payload.items.length} 个方向建议`;

  payload.items.forEach((item) => {
    const card = directionTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".direction-category").textContent = item.category;
    card.querySelector(".direction-name").textContent = item.title;
    card.querySelector(".direction-score").textContent = `匹配分 ${item.score.toFixed(2)}`;
    card.querySelector(".direction-description").textContent = item.description;
    card.querySelector(".direction-scene").textContent = item.target_scene;
    card.querySelector(".direction-budget").textContent = `预算 ¥${item.budget_min}-${item.budget_max}`;
    card.querySelector(".direction-difficulty").textContent = item.difficulty_level;

    const reasonContainer = card.querySelector(".direction-reasons");
    item.reasons.forEach((reason) => {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = reason;
      reasonContainer.appendChild(tag);
    });

    const starterList = card.querySelector(".starter-list");
    item.starter_products.forEach((product) => {
      const starter = document.createElement("div");
      starter.className = "starter-item";
      starter.textContent = `${product.product_role} · ${product.title} · ¥${product.price}`;
      starterList.appendChild(starter);
    });

    const actionButton = card.querySelector(".direction-action-button");
    actionButton.addEventListener("click", () => {
      navigateToProductStage(item.direction_id, item.title);
    });

    directionGrid.appendChild(card);
  });
}

function applyDirectionFilter(directionId, directionTitle) {
  selectedDirectionId = directionId;
  selectedDirectionTitle = directionTitle;
  renderProductStageHeader();
}

function clearDirectionFilter() {
  navigateToProductStage();
}

async function openProductDetail(userId, productId, scene, explanationData = null) {
  activeProductId = productId;
  activeUserId = userId;
  activeScene = scene;
  detailEventStatus.textContent = "正在打开商品详情...";

  await recordEvent({
    userId,
    productId,
    eventType: "click",
    scene,
  });

  try {
    const response = await fetch(`${API_BASE_URL}/api/products/${encodeURIComponent(productId)}`);

    if (!response.ok) {
      throw new Error(`商品服务返回 ${response.status}`);
    }

    const product = await response.json();
    renderProductDetail(product, explanationData);

    if (!productDialog.open) {
      productDialog.showModal();
    }
    await recordEvent({
      userId,
      productId,
      eventType: "view",
      scene,
    });
    detailEventStatus.textContent = "已记录：点击和浏览详情";
    loadAnalytics();
  } catch (error) {
    setStatus(`无法打开商品详情：${error.message}`, true);
  }
}

function renderProductDetail(product, explanationData = null) {
  document.querySelector("#dialog-image").src = product.image_url;
  document.querySelector("#dialog-image").alt = product.title;
  document.querySelector("#dialog-category").textContent = product.category;
  document.querySelector("#dialog-title").textContent = product.title;
  document.querySelector("#dialog-price").textContent = `${product.brand} · ¥${product.price}`;
  document.querySelector("#dialog-description").textContent = product.description;
  document.querySelector("#dialog-brand").textContent = product.brand;
  document.querySelector("#dialog-rating").textContent = product.rating.toFixed(1);
  document.querySelector("#dialog-stock").textContent = `${product.stock} 件`;

  const tagContainer = document.querySelector("#dialog-tags");
  tagContainer.innerHTML = "";
  product.features.forEach((feature) => {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = feature;
    tagContainer.appendChild(tag);
  });

  const explanationSection = document.querySelector(".dialog-explanation");
  const explanationTagContainer = document.querySelector("#dialog-explanation-tags");
  const explanationText = document.querySelector("#dialog-explanation-text");
  const feedbackStatus = document.querySelector("#dialog-feedback-status");

  if (explanationData && (explanationData.text || (explanationData.tags && explanationData.tags.length))) {
    explanationSection.style.display = "";
    explanationTagContainer.innerHTML = "";
    (explanationData.tags || []).forEach((t) => {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = t;
      explanationTagContainer.appendChild(tag);
    });
    explanationText.textContent = explanationData.text || "";
    feedbackStatus.textContent = "";

    const helpfulBtn = document.querySelector("#dialog-feedback-helpful");
    const inaccurateBtn = document.querySelector("#dialog-feedback-inaccurate");
    const freshHelpful = helpfulBtn.cloneNode(true);
    const freshInaccurate = inaccurateBtn.cloneNode(true);
    helpfulBtn.replaceWith(freshHelpful);
    inaccurateBtn.replaceWith(freshInaccurate);

    freshHelpful.addEventListener("click", () => {
      submitFeedback({ userId: activeUserId, productId: activeProductId, feedbackType: "helpful", statusNode: feedbackStatus });
    });
    freshInaccurate.addEventListener("click", () => {
      submitFeedback({ userId: activeUserId, productId: activeProductId, feedbackType: "inaccurate", statusNode: feedbackStatus });
    });
  } else {
    explanationSection.style.display = "none";
  }
}

async function submitProductEvent(eventType) {
  if (!activeProductId) {
    return;
  }

  const actionLabel = {
    favorite: "收藏",
    add_to_cart: "加入购物车",
    dislike: "不感兴趣",
  }[eventType];

  detailEventStatus.textContent = `正在记录：${actionLabel}`;

  try {
    const payload = await recordEvent({
      userId: activeUserId,
      productId: activeProductId,
      eventType,
      scene: activeScene,
    });
    detailEventStatus.textContent = `已记录：${actionLabel}，当前事件数 ${payload.event_count}`;
    loadAnalytics();
  } catch (error) {
    detailEventStatus.textContent = `行为记录失败：${error.message}`;
  }
}

async function recordEvent({ userId, productId, eventType, scene }) {
  const response = await fetch(`${API_BASE_URL}/api/events`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: userId,
      product_id: productId,
      event_type: eventType,
      scene,
      request_id: latestRequestId,
    }),
  });

  if (!response.ok) {
    throw new Error(`埋点服务返回 ${response.status}`);
  }

  return response.json();
}

async function submitFeedback({ userId, productId, feedbackType, statusNode }) {
  statusNode.textContent = "正在提交反馈...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/explanation-feedback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        product_id: productId,
        explanation_id: latestRequestId,
        feedback_type: feedbackType,
      }),
    });

    if (!response.ok) {
      throw new Error(`反馈服务返回 ${response.status}`);
    }

    statusNode.textContent = feedbackType === "helpful" ? "已记录：解释有帮助" : "已记录：解释不准确";
    loadAnalytics();
  } catch (error) {
    statusNode.textContent = `反馈提交失败：${error.message}`;
  }
}

async function loadAnalytics() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analytics/summary`);

    if (!response.ok) {
      throw new Error(`统计服务返回 ${response.status}`);
    }

    const payload = await response.json();
    renderAnalytics(payload);
  } catch (error) {
    metricGrid.innerHTML = "";
    topProductList.innerHTML = `<p class="analytics-error">无法加载统计：${error.message}</p>`;
  }
}

function renderAnalytics(payload) {
  const metrics = [
    ["推荐请求", payload.recommendation_request_count],
    ["商品曝光", payload.impression_count],
    ["商品点击", payload.click_count],
    ["点击率", formatPercent(payload.ctr)],
    ["加购次数", payload.add_to_cart_count],
    ["加购率", formatPercent(payload.add_to_cart_rate)],
    ["解释反馈", payload.feedback_count],
    ["解释有用率", formatPercent(payload.helpful_feedback_rate)],
  ];

  metricGrid.innerHTML = "";
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    metricGrid.appendChild(card);
  });

  topProductList.innerHTML = "";
  if (!payload.top_products.length) {
    topProductList.innerHTML = "<p class=\"analytics-empty\">暂无商品表现数据</p>";
    return;
  }

  payload.top_products.forEach((product) => {
    const row = topProductTemplate.content.firstElementChild.cloneNode(true);
    row.querySelector(".top-product-title").textContent = product.title;
    row.querySelector(".top-product-meta").textContent =
      `曝光 ${product.impressions} · 点击 ${product.clicks} · 加购 ${product.add_to_cart} · 收藏 ${product.favorites}`;
    row.querySelector(".top-product-ctr").textContent = `CTR ${formatPercent(product.ctr)}`;
    topProductList.appendChild(row);
  });
}

async function loadTrendManagement() {
  trendStatus.textContent = "正在加载趋势来源...";

  try {
    const [trendResponse, productResponse, adapterResponse] = await Promise.all([
      fetch(`${API_BASE_URL}/api/product-trends`),
      fetch(`${API_BASE_URL}/api/products`),
      fetch(`${API_BASE_URL}/api/product-trend-adapters`),
    ]);

    if (!trendResponse.ok) {
      throw new Error(`趋势服务返回 ${trendResponse.status}`);
    }

    if (!productResponse.ok) {
      throw new Error(`商品服务返回 ${productResponse.status}`);
    }

    if (!adapterResponse.ok) {
      throw new Error(`适配器服务返回 ${adapterResponse.status}`);
    }

    const trendPayload = await trendResponse.json();
    const productPayload = await productResponse.json();
    const adapterPayload = await adapterResponse.json();

    trendRecords = trendPayload.items;
    productCatalog = productPayload.items;
    trendAdapters = adapterPayload.items;
    populateTrendFilters();
    populateTrendAdapterSelect();
    renderTrendManagement();
  } catch (error) {
    trendMetricGrid.innerHTML = "";
    trendList.innerHTML = "";
    trendStatus.textContent = `无法加载趋势来源：${error.message}`;
  }
}

function populateTrendFilters() {
  const previousSource = trendSourceFilter.value;
  const previousCategory = trendCategoryFilter.value;
  const sourceOptions = Array.from(new Set(trendRecords.map((item) => item.source))).sort();
  const categoryOptions = Array.from(new Set(trendRecords.map((item) => item.category))).sort();

  resetSelectOptions(trendSourceFilter, "全部来源", sourceOptions, previousSource);
  resetSelectOptions(trendCategoryFilter, "全部品类", categoryOptions, previousCategory);
  populateTrendCreateProductSelect();
}

function resetSelectOptions(selectNode, emptyLabel, values, previousValue) {
  selectNode.innerHTML = "";
  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = emptyLabel;
  selectNode.appendChild(defaultOption);

  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    selectNode.appendChild(option);
  });

  if (previousValue && values.includes(previousValue)) {
    selectNode.value = previousValue;
  }
}

function renderTrendManagement() {
  const sourceFilter = trendSourceFilter.value;
  const categoryFilter = trendCategoryFilter.value;
  const productById = new Map(productCatalog.map((product) => [product.product_id, product]));
  const filteredRecords = trendRecords.filter((item) => {
    if (sourceFilter && item.source !== sourceFilter) {
      return false;
    }
    if (categoryFilter && item.category !== categoryFilter) {
      return false;
    }
    return true;
  });

  const mappedCount = filteredRecords.filter((item) => item.product_id && productById.has(item.product_id)).length;
  const unmappedCount = filteredRecords.length - mappedCount;
  const sourceCount = new Set(filteredRecords.map((item) => item.source)).size;
  const averageTrendScore = filteredRecords.length
    ? (filteredRecords.reduce((sum, item) => sum + item.trend_score, 0) / filteredRecords.length).toFixed(1)
    : "0.0";

  trendMetricGrid.innerHTML = "";
  const metrics = [
    ["趋势记录", filteredRecords.length],
    ["来源数量", sourceCount],
    ["已映射商品", mappedCount],
    ["平均热度分", averageTrendScore],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    trendMetricGrid.appendChild(card);
  });

  trendList.innerHTML = "";
  if (!filteredRecords.length) {
    trendStatus.textContent = "当前筛选条件下没有趋势记录";
    trendList.innerHTML = "<p class=\"analytics-empty\">没有找到匹配的趋势来源记录</p>";
    return;
  }

  trendStatus.textContent = `已加载 ${filteredRecords.length} 条趋势记录，其中 ${mappedCount} 条已映射商品，${unmappedCount} 条待确认`;

  filteredRecords
    .slice()
    .sort((left, right) => right.trend_score - left.trend_score || right.sales_score - left.sales_score)
    .forEach((item) => {
      const row = trendRowTemplate.content.firstElementChild.cloneNode(true);
      const mappedProduct = item.product_id ? productById.get(item.product_id) : null;
      const selectNode = row.querySelector(".trend-product-select");
      const saveButton = row.querySelector(".trend-save-button");
      const trendScoreInput = row.querySelector(".trend-score-input");
      const salesScoreInput = row.querySelector(".sales-score-input");
      const updateButton = row.querySelector(".trend-update-button");
      const deleteButton = row.querySelector(".trend-delete-button");
      const statusNode = row.querySelector(".trend-mapping-status");

      row.querySelector(".trend-source-badge").textContent = item.source;
      row.querySelector(".trend-category-badge").textContent = item.category;
      row.querySelector(".trend-keyword").textContent = item.keyword;
      row.querySelector(".trend-score-badge").textContent = `热度 ${Number(item.trend_score).toFixed(1)}`;
      row.querySelector(".sales-score-badge").textContent = `销量 ${Number(item.sales_score).toFixed(1)}`;
      row.querySelector(".trend-product-link").textContent = mappedProduct
        ? `已映射商品：${mappedProduct.title} (${mappedProduct.product_id})`
        : "尚未映射到现有商品";

      populateTrendProductSelect(selectNode, item, productCatalog);
      trendScoreInput.value = Number(item.trend_score).toFixed(1);
      salesScoreInput.value = Number(item.sales_score).toFixed(1);
      statusNode.textContent = mappedProduct
        ? "当前映射已生效"
        : "当前还没有映射，保存后会参与后续推荐和统计";

      saveButton.addEventListener("click", (e) => {
        withButtonLoading(e.currentTarget, "保存中...", () => saveTrendProductMapping({
          trendId: item.trend_id,
          nextProductId: selectNode.value || null,
          currentProductId: item.product_id || null,
          statusNode,
        }));
      });

      updateButton.addEventListener("click", (e) => {
        withButtonLoading(e.currentTarget, "保存中...", () => saveTrendScores({
          trendId: item.trend_id,
          currentTrendScore: Number(item.trend_score),
          currentSalesScore: Number(item.sales_score),
          nextTrendScore: parseTrendNumberInput(trendScoreInput.value),
          nextSalesScore: parseTrendNumberInput(salesScoreInput.value),
          statusNode,
        }));
      });

      deleteButton.addEventListener("click", (e) => {
        withButtonLoading(e.currentTarget, "删除中...", () => deleteTrendRecord({
          trendId: item.trend_id,
          keyword: item.keyword,
          statusNode,
        }));
      });

      makeRowCollapsible(row);
      trendList.appendChild(row);
    });
}

function populateTrendCreateProductSelect() {
  const previousValue = trendCreateProductSelect.value;
  const products = productCatalog
    .slice()
    .sort((left, right) => left.title.localeCompare(right.title, "zh-CN"));

  trendCreateProductSelect.innerHTML = "";
  const emptyOption = document.createElement("option");
  emptyOption.value = "";
  emptyOption.textContent = "暂不映射到商品";
  trendCreateProductSelect.appendChild(emptyOption);

  products.forEach((product) => {
    const option = document.createElement("option");
    option.value = product.product_id;
    option.textContent = `${product.title} (${product.product_id})`;
    trendCreateProductSelect.appendChild(option);
  });

  if (previousValue && products.some((product) => product.product_id === previousValue)) {
    trendCreateProductSelect.value = previousValue;
  }
}

function populateTrendAdapterSelect() {
  const previousValue = trendImportAdapterSelect.value;
  trendImportAdapterSelect.innerHTML = "";

  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = "自动识别";
  trendImportAdapterSelect.appendChild(defaultOption);

  trendAdapters.forEach((adapter) => {
    const option = document.createElement("option");
    option.value = adapter.name;
    option.textContent = `${adapter.name} · ${adapter.description}`;
    trendImportAdapterSelect.appendChild(option);
  });

  if (previousValue && trendAdapters.some((adapter) => adapter.name === previousValue)) {
    trendImportAdapterSelect.value = previousValue;
  }
}

function populateTrendProductSelect(selectNode, trendItem, products) {
  const currentValue = trendItem.product_id || "";
  const rankedProducts = products
    .slice()
    .sort((left, right) => rankTrendProductOption(trendItem, right) - rankTrendProductOption(trendItem, left));

  selectNode.innerHTML = "";

  const emptyOption = document.createElement("option");
  emptyOption.value = "";
  emptyOption.textContent = "暂不映射到商品";
  selectNode.appendChild(emptyOption);

  rankedProducts.forEach((product) => {
    const option = document.createElement("option");
    option.value = product.product_id;
    option.textContent = `${product.title} (${product.product_id})`;
    selectNode.appendChild(option);
  });

  selectNode.value = currentValue;
}

function rankTrendProductOption(trendItem, product) {
  let score = 0;
  const keyword = trendItem.keyword.toLowerCase();
  const productTerms = [
    product.title.toLowerCase(),
    product.brand.toLowerCase(),
    product.category.toLowerCase(),
    ...product.features.map((feature) => feature.toLowerCase()),
  ];

  if (trendItem.category === product.category) {
    score += 4;
  }

  if (keyword && product.title.toLowerCase().includes(keyword)) {
    score += 6;
  }

  splitTrendTerms(keyword).forEach((term) => {
    if (productTerms.some((productTerm) => productTerm.includes(term))) {
      score += 2;
    }
  });

  return score;
}

function splitTrendTerms(text) {
  return text
    .split(/[\s,/|、-]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

async function saveTrendProductMapping({ trendId, nextProductId, currentProductId, statusNode }) {
  if (nextProductId === currentProductId) {
    statusNode.textContent = nextProductId ? "映射没有变化" : "当前仍然是不映射状态";
    return;
  }

  statusNode.textContent = "正在保存映射...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-trends/${encodeURIComponent(trendId)}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        product_id: nextProductId,
      }),
    });

    if (!response.ok) {
      throw new Error(`趋势映射保存失败 ${response.status}`);
    }

    const updatedTrend = await response.json();
    trendRecords = trendRecords.map((item) => (item.trend_id === trendId ? updatedTrend : item));
    statusNode.textContent = updatedTrend.product_id ? "已保存新的商品映射" : "已清除商品映射";
    renderTrendManagement();
  } catch (error) {
    statusNode.textContent = `保存失败：${error.message}`;
  }
}


function parseTrendNumberInput(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : null;
}


async function saveTrendScores({
  trendId,
  currentTrendScore,
  currentSalesScore,
  nextTrendScore,
  nextSalesScore,
  statusNode,
}) {
  if (nextTrendScore === null || nextSalesScore === null) {
    statusNode.textContent = "请输入有效的热度分和销量分";
    return;
  }

  if (nextTrendScore === currentTrendScore && nextSalesScore === currentSalesScore) {
    statusNode.textContent = "分数没有变化";
    return;
  }

  statusNode.textContent = "正在保存分数...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-trends/${encodeURIComponent(trendId)}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        trend_score: nextTrendScore,
        sales_score: nextSalesScore,
      }),
    });

    if (!response.ok) {
      throw new Error(`趋势分数保存失败 ${response.status}`);
    }

    const updatedTrend = await response.json();
    trendRecords = trendRecords.map((item) => (item.trend_id === trendId ? updatedTrend : item));
    statusNode.textContent = "已保存新的热度分和销量分";
    renderTrendManagement();
  } catch (error) {
    statusNode.textContent = `保存失败：${error.message}`;
  }
}


async function deleteTrendRecord({ trendId, keyword, statusNode }) {
  const confirmed = window.confirm(`确定删除趋势记录“${keyword}”吗？这条记录会从 SQLite 中移除。`);
  if (!confirmed) {
    return;
  }

  statusNode.textContent = "正在删除记录...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-trends/${encodeURIComponent(trendId)}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`删除趋势记录失败 ${response.status}`);
    }

    trendRecords = trendRecords.filter((item) => item.trend_id !== trendId);
    statusNode.textContent = "已删除趋势记录";
    populateTrendFilters();
    renderTrendManagement();
  } catch (error) {
    statusNode.textContent = `删除失败：${error.message}`;
  }
}

async function createTrendRecord() {
  const source = trendCreateSourceInput.value.trim();
  const keyword = trendCreateKeywordInput.value.trim();
  const category = trendCreateCategoryInput.value.trim();
  const trendScore = parseTrendNumberInput(trendCreateScoreInput.value);
  const salesScore = parseTrendNumberInput(trendCreateSalesScoreInput.value);
  const productId = trendCreateProductSelect.value || null;

  if (!source || !keyword || !category) {
    trendCreateStatus.textContent = "请先填写来源、关键词和品类";
    return;
  }

  if (trendScore === null || salesScore === null) {
    trendCreateStatus.textContent = "请填写有效的热度分和销量分";
    return;
  }

  trendCreateStatus.textContent = "正在新增趋势记录...";

  try {
    const payload = {
      trend_id: buildNewTrendId(source, keyword, category),
      product_id: productId,
      source,
      keyword,
      category,
      trend_score: trendScore,
      sales_score: salesScore,
    };

    const response = await fetch(`${API_BASE_URL}/api/product-trends`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`新增趋势记录失败 ${response.status}`);
    }

    const createdTrend = await response.json();
    trendRecords = [createdTrend, ...trendRecords];
    populateTrendFilters();
    renderTrendManagement();
    resetTrendCreateForm(source, category);
    trendCreateStatus.textContent = "已新增趋势记录";
  } catch (error) {
    trendCreateStatus.textContent = `新增失败：${error.message}`;
  }
}

async function importTrendBatch() {
  const draft = await buildTrendImportDraft();
  if (!draft) {
    trendImportStatus.textContent = "请先选择文件，或者粘贴 JSON / CSV 内容";
    return;
  }

  trendImportStatus.textContent = "正在批量导入趋势记录...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-trends/batch-import`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(draft),
    });

    if (!response.ok) {
      let detail = `批量导入失败 ${response.status}`;
      try {
        const payload = await response.json();
        if (payload.detail) {
          detail = payload.detail;
        }
      } catch (error) {
        // ignore malformed error body
      }
      throw new Error(detail);
    }

    const payload = await response.json();
    trendImportStatus.textContent =
      `已导入 ${payload.imported_count} 条趋势记录，自动映射 ${payload.mapped_count} 条，使用适配器 ${payload.adapter}`;
    trendImportForm.reset();
    clearTrendPreview();
    loadTrendManagement();
    loadImportHistory();
  } catch (error) {
    trendImportStatus.textContent = `导入失败：${error.message}`;
    loadImportHistory();
  }
}

async function previewTrendBatch() {
  const draft = await buildTrendImportDraft();
  if (!draft) {
    trendPreviewStatus.textContent = "请先选择文件，或者粘贴 JSON / CSV 内容";
    return;
  }

  trendPreviewStatus.textContent = "正在生成导入预览...";
  trendPreviewMetricGrid.innerHTML = "";
  trendPreviewList.innerHTML = "";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-trends/batch-preview`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(draft),
    });

    if (!response.ok) {
      let detail = `导入预览失败 ${response.status}`;
      try {
        const payload = await response.json();
        if (payload.detail) {
          detail = payload.detail;
        }
      } catch (error) {
        // ignore malformed error body
      }
      throw new Error(detail);
    }

    const payload = await response.json();
    renderTrendImportPreview(payload);
    loadImportHistory();
  } catch (error) {
    trendPreviewStatus.textContent = `预览失败：${error.message}`;
    loadImportHistory();
  }
}

async function buildTrendImportDraft() {
  const selectedFile = trendImportFileInput.files?.[0] || null;
  const manualContent = trendImportContentInput.value.trim();
  const adapter = trendImportAdapterSelect.value || null;

  let content = manualContent;
  let filename = manualContent.startsWith("[") ? "pasted_trends.json" : "pasted_trends.csv";

  if (selectedFile) {
    content = await selectedFile.text();
    filename = selectedFile.name;
  }

  if (!content.trim()) {
    return null;
  }

  return {
    content,
    filename,
    adapter,
  };
}

function renderTrendImportPreview(payload) {
  trendPreviewStatus.textContent =
    `预览完成：共 ${payload.total_count} 条，${payload.ready_count} 条可导入，${payload.error_count} 条有问题，使用适配器 ${payload.adapter}`;

  renderTrendPresetPanel(payload);

  trendPreviewMetricGrid.innerHTML = "";
  const metrics = [
    ["总条数", payload.total_count],
    ["可导入", payload.ready_count],
    ["错误条数", payload.error_count],
    ["自动映射", payload.mapped_count],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    trendPreviewMetricGrid.appendChild(card);
  });

  trendPreviewList.innerHTML = "";
  payload.items.forEach((item) => {
    const row = trendPreviewRowTemplate.content.firstElementChild.cloneNode(true);
    const isReady = item.status === "ready";
    row.classList.toggle("is-error", !isReady);

    row.querySelector(".trend-preview-status-badge").textContent = isReady ? "可导入" : "有问题";
    row.querySelector(".trend-preview-status-badge").classList.toggle("is-error", !isReady);
    row.querySelector(".trend-preview-row-number").textContent = `第 ${item.row_number} 行`;
    row.querySelector(".trend-preview-keyword").textContent = item.keyword || "无法解析关键词";
    row.querySelector(".trend-preview-trend-score").textContent =
      item.trend_score !== null && item.trend_score !== undefined ? `热度 ${Number(item.trend_score).toFixed(1)}` : "热度 -";
    row.querySelector(".trend-preview-sales-score").textContent =
      item.sales_score !== null && item.sales_score !== undefined ? `销量 ${Number(item.sales_score).toFixed(1)}` : "销量 -";
    row.querySelector(".trend-preview-meta").textContent = item.source && item.category
      ? `${item.source} · ${item.category}`
      : "该行字段不完整";
    row.querySelector(".trend-preview-detail").textContent = isReady
      ? buildTrendPreviewDetail(item)
      : item.error || "该行存在无法导入的问题";

    trendPreviewList.appendChild(row);
  });
}

function renderTrendPresetPanel(payload) {
  const mappedHeaders = payload.mapped_headers || [];
  const unmappedHeaders = payload.unmapped_headers || [];
  const detectedHeaders = payload.detected_headers || [];

  const mappedMarkup = mappedHeaders.length
    ? mappedHeaders
        .map((item) => `<span class="preset-mapping-chip">${escapeHtml(item.source_field)} -> ${escapeHtml(item.target_field)}</span>`)
        .join("")
    : "<p class=\"preset-empty\">这次没有识别到可映射字段。</p>";

  const unmappedMarkup = unmappedHeaders.length
    ? unmappedHeaders
        .map((header) => `<span class="preset-unmapped-chip">${escapeHtml(header)}</span>`)
        .join("")
    : "<span class=\"preset-ok\">没有额外未识别字段</span>";

  const detectedMarkup = detectedHeaders.length
    ? detectedHeaders
        .map((header) => `<span class="preset-detected-chip">${escapeHtml(header)}</span>`)
        .join("")
    : "<span class=\"preset-empty\">当前内容里还没有可识别表头</span>";

  trendPresetPanel.innerHTML = `
    <div class="preset-section">
      <p class="preset-label">识别到的平台模板</p>
      <strong class="preset-title">${escapeHtml(payload.adapter)}</strong>
      <p class="preset-description">${escapeHtml(payload.adapter_description || "未提供模板描述")}</p>
    </div>
    <div class="preset-section">
      <p class="preset-label">检测到的原始字段</p>
      <div class="preset-chip-list">${detectedMarkup}</div>
    </div>
    <div class="preset-section">
      <p class="preset-label">字段映射预设</p>
      <div class="preset-chip-list">${mappedMarkup}</div>
    </div>
    <div class="preset-section">
      <p class="preset-label">未使用字段</p>
      <div class="preset-chip-list">${unmappedMarkup}</div>
    </div>
  `;
}

function buildTrendPreviewDetail(item) {
  const segments = [];
  if (item.generated_trend_id) {
    segments.push(`自动生成 trend_id：${item.trend_id}`);
  } else if (item.trend_id) {
    segments.push(`trend_id：${item.trend_id}`);
  }

  if (item.product_id && item.mapped_product_title) {
    segments.push(
      item.auto_mapped
        ? `自动映射商品：${item.mapped_product_title} (${item.product_id})`
        : `商品映射：${item.mapped_product_title} (${item.product_id})`
    );
  } else if (item.product_id) {
    segments.push(`商品映射：${item.product_id}`);
  } else {
    segments.push("没有商品映射");
  }

  return segments.join(" · ");
}

function clearTrendPreview() {
  trendPreviewStatus.textContent = "点击“先预览导入结果”后，这里会显示可导入条数、错误条数和自动映射情况。";
  trendPresetPanel.innerHTML = "";
  trendPreviewMetricGrid.innerHTML = "";
  trendPreviewList.innerHTML = "";
}

async function loadProductSourceManagement() {
  productSourceStatus.textContent = "正在加载商品来源...";

  try {
    const [productResponse, adapterResponse] = await Promise.all([
      fetch(`${API_BASE_URL}/api/products`),
      fetch(`${API_BASE_URL}/api/product-source-adapters`),
    ]);

    if (!productResponse.ok) {
      throw new Error(`商品服务返回 ${productResponse.status}`);
    }

    if (!adapterResponse.ok) {
      throw new Error(`商品适配器服务返回 ${adapterResponse.status}`);
    }

    const productPayload = await productResponse.json();
    const adapterPayload = await adapterResponse.json();

    productCatalog = productPayload.items;
    productSourceAdapters = adapterPayload.items;
    populateProductSourceFilters();
    populateProductAdapterSelect();
    populateProductSyncAdapterSelect();
    renderProductSourceManagement();
    renderProductManagement();
    if (directionCatalog.length) {
      renderDirectionManagement();
    }
  } catch (error) {
    productSourceMetricGrid.innerHTML = "";
    productSourceList.innerHTML = "";
    productSourceStatus.textContent = `无法加载商品来源：${error.message}`;
    productManagementMetricGrid.innerHTML = "";
    productManagementList.innerHTML = "";
    productManagementStatus.textContent = `无法加载商品管理数据：${error.message}`;
  }
}

async function loadProductSyncManagement() {
  productSyncStatus.textContent = "正在加载自动同步来源...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-sync-sources`);
    if (!response.ok) {
      throw new Error(`商品同步来源服务返回 ${response.status}`);
    }

    const payload = await response.json();
    productSyncSources = payload.items || [];
    renderProductSyncManagement();
  } catch (error) {
    productSyncMetricGrid.innerHTML = "";
    productSyncList.innerHTML = "";
    productSyncStatus.textContent = `无法加载自动同步来源：${error.message}`;
  }
}

async function loadImportHistory() {
  importHistoryStatus.textContent = "正在加载导入历史...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/import-history?limit=50`);
    if (!response.ok) {
      throw new Error(`导入历史服务返回 ${response.status}`);
    }

    const payload = await response.json();
    importHistoryRecords = payload.items || [];
    renderImportHistory();
  } catch (error) {
    importHistoryMetricGrid.innerHTML = "";
    importHistoryList.innerHTML = "";
    importHistoryStatus.textContent = `无法加载导入历史：${error.message}`;
  }
}

async function loadUserManagement() {
  userManagementStatus.textContent = "正在加载用户画像...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/users`);
    if (!response.ok) {
      throw new Error(`用户服务返回 ${response.status}`);
    }

    const payload = await response.json();
    userProfiles = payload.items || [];
    populateUserSelect();
    renderUserManagement();
  } catch (error) {
    userManagementMetricGrid.innerHTML = "";
    userManagementList.innerHTML = "";
    userManagementStatus.textContent = `无法加载用户画像：${error.message}`;
  }
}

async function loadDirectionManagement() {
  directionManagementStatus.textContent = "正在加载方向管理数据...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/directions`);
    if (!response.ok) {
      throw new Error(`方向服务返回 ${response.status}`);
    }

    const payload = await response.json();
    directionCatalog = payload.items || [];

    const linkPayloads = await Promise.all(
      directionCatalog.map(async (direction) => {
        const linkResponse = await fetch(
          `${API_BASE_URL}/api/directions/${encodeURIComponent(direction.direction_id)}/products`
        );
        if (!linkResponse.ok) {
          throw new Error(`方向商品映射服务返回 ${linkResponse.status}`);
        }
        const linkPayload = await linkResponse.json();
        return linkPayload.items || [];
      })
    );

    directionProductLinks = linkPayloads.flat();
    populateDirectionFilters();
    renderDirectionManagement();
    if (selectedDirectionId) {
      renderDirectionLayerPanel();
    }
  } catch (error) {
    directionManagementMetricGrid.innerHTML = "";
    directionManagementList.innerHTML = "";
    directionManagementStatus.textContent = `无法加载方向管理数据：${error.message}`;
  }
}

function populateUserSelect() {
  const previousValue = userSelect.value;
  userSelect.innerHTML = "";

  userProfiles
    .slice()
    .sort((left, right) => left.user_id.localeCompare(right.user_id, "zh-CN"))
    .forEach((user) => {
      const option = document.createElement("option");
      option.value = user.user_id;
      option.textContent = user.username;
      userSelect.appendChild(option);
    });

  if (previousValue && userProfiles.some((user) => user.user_id === previousValue)) {
    userSelect.value = previousValue;
  }
}

function populateDirectionFilters() {
  const categoryOptions = Array.from(new Set(directionCatalog.map((item) => item.category))).sort();
  const difficultyOptions = Array.from(new Set(directionCatalog.map((item) => item.difficulty_level))).sort();

  resetSelectOptions(
    directionManagementCategoryFilter,
    "全部品类",
    categoryOptions,
    directionManagementCategoryFilter.value
  );
  resetSelectOptions(
    directionManagementDifficultyFilter,
    "全部难度",
    difficultyOptions,
    directionManagementDifficultyFilter.value
  );
}

function renderUserManagement() {
  const budgetFilter = userBudgetFilter.value;
  const interestKeyword = userInterestFilter.value.trim().toLowerCase();
  const filteredUsers = userProfiles.filter((user) => {
    const budgetSpan = Number(user.price_max || 0) - Number(user.price_min || 0);
    if (budgetFilter === "low" && Number(user.price_max || 0) > 200) {
      return false;
    }
    if (budgetFilter === "mid" && (Number(user.price_max || 0) <= 200 || Number(user.price_max || 0) > 600)) {
      return false;
    }
    if (budgetFilter === "high" && Number(user.price_max || 0) <= 600) {
      return false;
    }

    if (!interestKeyword) {
      return true;
    }

    const haystack = [
      ...(user.long_term_interests || []),
      ...(user.recent_interests || []),
      ...(user.brand_preference || []),
      ...(user.negative_tags || []),
      user.username || "",
      user.user_id || "",
    ]
      .join(" ")
      .toLowerCase();

    return haystack.includes(interestKeyword) || budgetSpan.toString().includes(interestKeyword);
  });

  const averageBudget = filteredUsers.length
    ? (
        filteredUsers.reduce((sum, user) => sum + (Number(user.price_max || 0) - Number(user.price_min || 0)), 0) /
        filteredUsers.length
      ).toFixed(0)
    : "0";
  const runningUsers = filteredUsers.filter((user) =>
    [...(user.long_term_interests || []), ...(user.recent_interests || [])].some((item) => item.includes("跑"))
  ).length;
  const coffeeUsers = filteredUsers.filter((user) =>
    [...(user.long_term_interests || []), ...(user.recent_interests || [])].some((item) => item.includes("咖啡"))
  ).length;

  userManagementMetricGrid.innerHTML = "";
  const metrics = [
    ["用户数", filteredUsers.length],
    ["平均预算跨度", averageBudget],
    ["跑步兴趣用户", runningUsers],
    ["咖啡兴趣用户", coffeeUsers],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    userManagementMetricGrid.appendChild(card);
  });

  userManagementList.innerHTML = "";
  if (!filteredUsers.length) {
    userManagementStatus.textContent = "当前筛选条件下没有用户画像";
    userManagementList.innerHTML = "<p class=\"analytics-empty\">还没有匹配的用户画像</p>";
    return;
  }

  userManagementStatus.textContent = `已加载 ${filteredUsers.length} 个用户画像，可直接编辑并保存`;

  filteredUsers
    .slice()
    .sort((left, right) => left.user_id.localeCompare(right.user_id, "zh-CN"))
    .forEach((user) => {
      const row = userManagementRowTemplate.content.firstElementChild.cloneNode(true);
      row.querySelector(".trend-source-badge").textContent = user.user_id;
      row.querySelector(".trend-category-badge").textContent = `预算 ${user.price_min}-${user.price_max}`;
      row.querySelector(".trend-keyword").textContent = user.username;
      row.querySelector(".trend-score-badge").textContent = `长期 ${(user.long_term_interests || []).length}`;
      row.querySelector(".sales-score-badge").textContent = `近期 ${(user.recent_interests || []).length}`;
      row.querySelector(".trend-product-link").textContent =
        `品牌偏好 ${(user.brand_preference || []).join(", ") || "无"} · 负向偏好 ${(user.negative_tags || []).join(", ") || "无"}`;

      row.querySelector(".user-edit-name").value = user.username || "";
      row.querySelector(".user-edit-price-min").value = user.price_min ?? 0;
      row.querySelector(".user-edit-price-max").value = user.price_max ?? 0;
      row.querySelector(".user-edit-long-interests").value = (user.long_term_interests || []).join(", ");
      row.querySelector(".user-edit-recent-interests").value = (user.recent_interests || []).join(", ");
      row.querySelector(".user-edit-brands").value = (user.brand_preference || []).join(", ");
      row.querySelector(".user-edit-negative-tags").value = (user.negative_tags || []).join(", ");

      const statusNode = row.querySelector(".trend-mapping-status");
      statusNode.textContent = "可以直接修改用户画像并保存";

      const userSaveBtn = row.querySelector(".user-save-button");
      userSaveBtn.addEventListener("click", () => {
        withButtonLoading(userSaveBtn, "保存中...", () => saveManagedUser(user.user_id, row, statusNode));
      });

      makeRowCollapsible(row);
      userManagementList.appendChild(row);
    });
}

function renderDirectionManagement() {
  const categoryFilter = directionManagementCategoryFilter.value;
  const difficultyFilter = directionManagementDifficultyFilter.value;
  const filteredDirections = directionCatalog.filter((direction) => {
    if (categoryFilter && direction.category !== categoryFilter) {
      return false;
    }
    if (difficultyFilter && direction.difficulty_level !== difficultyFilter) {
      return false;
    }
    return true;
  });

  const categoryCount = new Set(filteredDirections.map((direction) => direction.category)).size;
  const linkedProductCount = new Set(
    directionProductLinks
      .filter((link) => filteredDirections.some((direction) => direction.direction_id === link.direction_id))
      .map((link) => link.product_id)
  ).size;
  const beginnerCount = filteredDirections.filter((direction) => (direction.difficulty_level || "").includes("入门")).length;
  const averageBudget = filteredDirections.length
    ? (
        filteredDirections.reduce(
          (sum, direction) => sum + (Number(direction.budget_max || 0) - Number(direction.budget_min || 0)),
          0
        ) / filteredDirections.length
      ).toFixed(0)
    : "0";

  directionManagementMetricGrid.innerHTML = "";
  const metrics = [
    ["方向数", filteredDirections.length],
    ["品类数", categoryCount],
    ["已关联商品数", linkedProductCount],
    ["入门方向数", beginnerCount],
    ["平均预算跨度", averageBudget],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    directionManagementMetricGrid.appendChild(card);
  });

  directionManagementList.innerHTML = "";
  if (!filteredDirections.length) {
    directionManagementStatus.textContent = "当前筛选条件下没有方向";
    directionManagementList.innerHTML = "<p class=\"analytics-empty\">还没有匹配的方向记录</p>";
    return;
  }

  directionManagementStatus.textContent = `已加载 ${filteredDirections.length} 个方向，可直接编辑方向信息和关联商品`;

  filteredDirections
    .slice()
    .sort((left, right) => left.title.localeCompare(right.title, "zh-CN"))
    .forEach((direction) => {
      const row = directionManagementRowTemplate.content.firstElementChild.cloneNode(true);
      const links = getDirectionLinks(direction.direction_id);
      const linkedProducts = links.map((link) => buildDirectionLinkLabel(link)).join("，");

      row.querySelector(".trend-source-badge").textContent = direction.direction_id;
      row.querySelector(".trend-category-badge").textContent = direction.category;
      row.querySelector(".trend-keyword").textContent = direction.title;
      row.querySelector(".trend-score-badge").textContent = direction.difficulty_level;
      row.querySelector(".sales-score-badge").textContent = `预算 ${direction.budget_min}-${direction.budget_max}`;
      row.querySelector(".trend-product-link").textContent =
        `${direction.target_scene} · 目标兴趣 ${(direction.target_interests || []).join(", ") || "无"} · 方向商品 ${linkedProducts || "未配置"}`;

      row.querySelector(".direction-edit-title").value = direction.title || "";
      row.querySelector(".direction-edit-category").value = direction.category || "";
      row.querySelector(".direction-edit-scene").value = direction.target_scene || "";
      row.querySelector(".direction-edit-difficulty").value = direction.difficulty_level || "";
      row.querySelector(".direction-edit-budget-min").value = direction.budget_min ?? 0;
      row.querySelector(".direction-edit-budget-max").value = direction.budget_max ?? 0;
      row.querySelector(".direction-edit-interests").value = (direction.target_interests || []).join(", ");
      buildDirectionProductSelector(row.querySelector(".direction-product-selector"), links, productCatalog);
      row.querySelector(".direction-edit-description").value = direction.description || "";

      const statusNode = row.querySelector(".trend-mapping-status");
      statusNode.textContent = links.length
        ? `当前已关联 ${links.length} 个商品`
        : "当前还没有配置方向商品";

      const directionSaveBtn = row.querySelector(".direction-save-button");
      directionSaveBtn.addEventListener("click", () => {
        withButtonLoading(directionSaveBtn, "保存中...", () => saveManagedDirection(direction.direction_id, row, statusNode));
      });

      makeRowCollapsible(row);
      directionManagementList.appendChild(row);
    });

  buildDirectionProductSelector(directionCreateProductSelector, [], productCatalog);
}

async function createManagedUser() {
  const userId = userCreateIdInput.value.trim();
  const username = userCreateNameInput.value.trim();
  if (!userId || !username) {
    userManagementStatus.textContent = "请至少填写用户 ID 和用户名";
    return;
  }

  const payload = {
    user_id: userId,
    username,
    long_term_interests: parseListInput(userCreateLongInterestsInput.value),
    recent_interests: parseListInput(userCreateRecentInterestsInput.value),
    brand_preference: parseListInput(userCreateBrandsInput.value),
    price_min: Math.max(0, Number(userCreatePriceMinInput.value || 0)),
    price_max: Math.max(0, Number(userCreatePriceMaxInput.value || 0)),
    negative_tags: parseListInput(userCreateNegativeTagsInput.value),
  };

  userManagementStatus.textContent = "正在新增用户画像...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`新增用户画像失败 ${response.status}`);
    }

    userCreateForm.reset();
    userManagementStatus.textContent = "已新增用户画像";
    loadUserManagement();
  } catch (error) {
    userManagementStatus.textContent = `新增失败：${error.message}`;
  }
}

async function createManagedDirection() {
  const directionId = directionCreateIdInput.value.trim();
  const title = directionCreateTitleInput.value.trim();
  const category = directionCreateCategoryInput.value.trim();
  const targetScene = directionCreateSceneInput.value.trim();
  const difficultyLevel = directionCreateDifficultyInput.value.trim();
  const budgetMin = Math.max(0, Number(directionCreateBudgetMinInput.value || 0));
  const budgetMax = Math.max(0, Number(directionCreateBudgetMaxInput.value || 0));

  if (!directionId || !title || !category || !targetScene || !difficultyLevel) {
    directionManagementStatus.textContent = "请至少填写方向 ID、标题、品类、目标场景和难度级别";
    return;
  }

  if (budgetMax < budgetMin) {
    directionManagementStatus.textContent = "预算上限不能小于预算下限";
    return;
  }

  const payload = {
    direction_id: directionId,
    title,
    category,
    description: directionCreateDescriptionInput.value.trim() || `${title} 方向说明`,
    target_scene: targetScene,
    budget_min: budgetMin,
    budget_max: budgetMax,
    difficulty_level: difficultyLevel,
    target_interests: parseListInput(directionCreateInterestsInput.value),
  };
  const directionLinks = readDirectionProductSelector(directionCreateProductSelector, directionId);

  directionManagementStatus.textContent = "正在新增方向...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/directions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`新增方向失败 ${response.status}`);
    }

    const linkResponse = await fetch(`${API_BASE_URL}/api/directions/${encodeURIComponent(directionId)}/products`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(directionLinks),
    });

    if (!linkResponse.ok) {
      throw new Error(`保存方向商品失败 ${linkResponse.status}`);
    }

    resetDirectionCreateForm();
    directionManagementStatus.textContent = "已新增方向";
    loadDirectionManagement();
  } catch (error) {
    directionManagementStatus.textContent = `新增失败：${error.message}`;
  }
}

async function saveManagedUser(userId, row, statusNode) {
  const priceMin = Math.max(0, Number(row.querySelector(".user-edit-price-min").value || 0));
  const priceMax = Math.max(0, Number(row.querySelector(".user-edit-price-max").value || 0));
  if (priceMax < priceMin) {
    statusNode.textContent = "预算上限不能小于预算下限";
    return;
  }

  const payload = {
    username: row.querySelector(".user-edit-name").value.trim(),
    price_min: priceMin,
    price_max: priceMax,
    long_term_interests: parseListInput(row.querySelector(".user-edit-long-interests").value),
    recent_interests: parseListInput(row.querySelector(".user-edit-recent-interests").value),
    brand_preference: parseListInput(row.querySelector(".user-edit-brands").value),
    negative_tags: parseListInput(row.querySelector(".user-edit-negative-tags").value),
  };

  if (!payload.username) {
    statusNode.textContent = "用户名不能为空";
    return;
  }

  statusNode.textContent = "正在保存用户画像...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/users/${encodeURIComponent(userId)}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`保存用户画像失败 ${response.status}`);
    }

    statusNode.textContent = "用户画像已保存";
    loadUserManagement();
  } catch (error) {
    statusNode.textContent = `保存失败：${error.message}`;
  }
}

async function saveManagedDirection(directionId, row, statusNode) {
  const budgetMin = Math.max(0, Number(row.querySelector(".direction-edit-budget-min").value || 0));
  const budgetMax = Math.max(0, Number(row.querySelector(".direction-edit-budget-max").value || 0));
  if (budgetMax < budgetMin) {
    statusNode.textContent = "预算上限不能小于预算下限";
    return;
  }

  const payload = {
    title: row.querySelector(".direction-edit-title").value.trim(),
    category: row.querySelector(".direction-edit-category").value.trim(),
    description: row.querySelector(".direction-edit-description").value.trim(),
    target_scene: row.querySelector(".direction-edit-scene").value.trim(),
    budget_min: budgetMin,
    budget_max: budgetMax,
    difficulty_level: row.querySelector(".direction-edit-difficulty").value.trim(),
    target_interests: parseListInput(row.querySelector(".direction-edit-interests").value),
  };

  if (!payload.title || !payload.category || !payload.target_scene || !payload.difficulty_level) {
    statusNode.textContent = "标题、品类、场景和难度级别不能为空";
    return;
  }

  const directionLinks = readDirectionProductSelector(
    row.querySelector(".direction-product-selector"),
    directionId
  );

  statusNode.textContent = "正在保存方向...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/directions/${encodeURIComponent(directionId)}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`保存方向失败 ${response.status}`);
    }

    const linkResponse = await fetch(`${API_BASE_URL}/api/directions/${encodeURIComponent(directionId)}/products`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(directionLinks),
    });

    if (!linkResponse.ok) {
      throw new Error(`保存方向商品失败 ${linkResponse.status}`);
    }

    statusNode.textContent = "方向已保存";
    loadDirectionManagement();
  } catch (error) {
    statusNode.textContent = `保存失败：${error.message}`;
  }
}

function renderImportHistory() {
  const entityFilter = importEntityFilter.value;
  const operationFilter = importOperationFilter.value;
  const filteredRecords = importHistoryRecords.filter((item) => {
    if (entityFilter && item.entity_type !== entityFilter) {
      return false;
    }
    if (operationFilter && item.operation !== operationFilter) {
      return false;
    }
    return true;
  });

  const successCount = filteredRecords.filter((item) => item.status === "success").length;
  const errorCount = filteredRecords.filter((item) => item.status === "error").length;
  const importCount = filteredRecords.filter((item) => item.operation === "import").length;
  const previewCount = filteredRecords.filter((item) => item.operation === "preview").length;

  importHistoryMetricGrid.innerHTML = "";
  const metrics = [
    ["记录数", filteredRecords.length],
    ["成功", successCount],
    ["失败", errorCount],
    ["预览", previewCount],
    ["正式导入", importCount],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    importHistoryMetricGrid.appendChild(card);
  });

  importHistoryList.innerHTML = "";
  if (!filteredRecords.length) {
    importHistoryStatus.textContent = "当前筛选条件下没有导入历史";
    importHistoryList.innerHTML = "<p class=\"analytics-empty\">还没有导入历史记录</p>";
    return;
  }

  importHistoryStatus.textContent = `已加载 ${filteredRecords.length} 条导入历史`;

  filteredRecords.forEach((item) => {
    const row = importHistoryRowTemplate.content.firstElementChild.cloneNode(true);
    row.querySelector(".trend-source-badge").textContent = item.entity_type === "product" ? "商品" : "趋势";
    row.querySelector(".trend-category-badge").textContent = item.operation === "import" ? "正式导入" : "预览";
    row.querySelector(".trend-keyword").textContent = item.filename || "未提供文件名";
    row.querySelector(".trend-score-badge").textContent = item.status === "success" ? "成功" : "失败";
    row.querySelector(".sales-score-badge").textContent = item.adapter || "auto";
    row.querySelector(".trend-product-link").textContent =
      `总条数 ${item.total_count} · 可处理 ${item.ready_count} · 错误 ${item.error_count} · 导入 ${item.imported_count}`;
    row.querySelector(".trend-mapping-status").textContent =
      `${item.created_at || ""} · 生成 ID ${item.generated_id_count} · 映射 ${item.mapped_count}${item.message ? ` · ${item.message}` : ""}`;
    importHistoryList.appendChild(row);
  });
}

function populateProductSourceFilters() {
  const previousSource = productSourceFilter.value;
  const previousCategory = productCategoryFilter.value;
  const sourceOptions = Array.from(new Set(productCatalog.map((item) => item.source))).sort();
  const categoryOptions = Array.from(new Set(productCatalog.map((item) => item.category))).sort();

  resetSelectOptions(productSourceFilter, "全部来源", sourceOptions, previousSource);
  resetSelectOptions(productCategoryFilter, "全部品类", categoryOptions, previousCategory);
  resetSelectOptions(productManagementSourceFilter, "全部来源", sourceOptions, productManagementSourceFilter.value);
  resetSelectOptions(productManagementCategoryFilter, "全部品类", categoryOptions, productManagementCategoryFilter.value);
}

function populateProductAdapterSelect() {
  const previousValue = productImportAdapterSelect.value;
  productImportAdapterSelect.innerHTML = "";

  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = "自动识别";
  productImportAdapterSelect.appendChild(defaultOption);

  productSourceAdapters.forEach((adapter) => {
    const option = document.createElement("option");
    option.value = adapter.name;
    option.textContent = `${adapter.name} · ${adapter.description}`;
    productImportAdapterSelect.appendChild(option);
  });

  if (previousValue && productSourceAdapters.some((adapter) => adapter.name === previousValue)) {
    productImportAdapterSelect.value = previousValue;
  }
}

function populateProductSyncAdapterSelect() {
  const previousValue = productSyncCreateAdapterSelect.value;
  productSyncCreateAdapterSelect.innerHTML = "";

  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = "自动识别";
  productSyncCreateAdapterSelect.appendChild(defaultOption);

  productSourceAdapters.forEach((adapter) => {
    const option = document.createElement("option");
    option.value = adapter.name;
    option.textContent = `${adapter.name} · ${adapter.description}`;
    productSyncCreateAdapterSelect.appendChild(option);
  });

  if (previousValue && productSourceAdapters.some((adapter) => adapter.name === previousValue)) {
    productSyncCreateAdapterSelect.value = previousValue;
  }
}

function renderProductSourceManagement() {
  const sourceFilter = productSourceFilter.value;
  const categoryFilter = productCategoryFilter.value;
  const filteredProducts = productCatalog.filter((item) => {
    if (sourceFilter && item.source !== sourceFilter) {
      return false;
    }
    if (categoryFilter && item.category !== categoryFilter) {
      return false;
    }
    return true;
  });

  const sourceCount = new Set(filteredProducts.map((item) => item.source)).size;
  const externalLinkedCount = filteredProducts.filter((item) => item.external_id).length;
  const averagePopularity = filteredProducts.length
    ? (filteredProducts.reduce((sum, item) => sum + (item.popularity_score || 0), 0) / filteredProducts.length).toFixed(1)
    : "0.0";
  const averageSales = filteredProducts.length
    ? (filteredProducts.reduce((sum, item) => sum + (item.sales_score || 0), 0) / filteredProducts.length).toFixed(1)
    : "0.0";

  productSourceMetricGrid.innerHTML = "";
  const metrics = [
    ["商品数", filteredProducts.length],
    ["来源数量", sourceCount],
    ["外部 ID 已绑定", externalLinkedCount],
    ["平均热度分", averagePopularity],
    ["平均销量分", averageSales],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    productSourceMetricGrid.appendChild(card);
  });

  productSourceList.innerHTML = "";
  if (!filteredProducts.length) {
    productSourceStatus.textContent = "当前筛选条件下没有商品来源记录";
    productSourceList.innerHTML = "<p class=\"analytics-empty\">还没有匹配的商品来源记录</p>";
    return;
  }

  productSourceStatus.textContent = `已加载 ${filteredProducts.length} 个商品，其中 ${externalLinkedCount} 个带外部 ID`;

  filteredProducts
    .slice()
    .sort((left, right) => {
      const scoreGap = (right.popularity_score || 0) - (left.popularity_score || 0);
      if (scoreGap !== 0) {
        return scoreGap;
      }
      return (right.sales_score || 0) - (left.sales_score || 0);
    })
    .forEach((item) => {
      const row = productSourceRowTemplate.content.firstElementChild.cloneNode(true);
      row.querySelector(".trend-source-badge").textContent = item.source || "manual";
      row.querySelector(".trend-category-badge").textContent = item.category;
      row.querySelector(".trend-keyword").textContent = item.title;
      row.querySelector(".trend-score-badge").textContent = `热度 ${Number(item.popularity_score || 0).toFixed(1)}`;
      row.querySelector(".sales-score-badge").textContent = `销量 ${Number(item.sales_score || 0).toFixed(1)}`;
      row.querySelector(".trend-product-link").textContent =
        `${item.brand} · ¥${item.price} · 库存 ${item.stock} · 评分 ${Number(item.rating).toFixed(1)}`;
      row.querySelector(".trend-mapping-status").textContent = item.external_id
        ? `商品 ID：${item.product_id} · 外部 ID：${item.external_id}`
        : `商品 ID：${item.product_id}`;
      productSourceList.appendChild(row);
    });
}

function renderProductSyncManagement() {
  const typeFilter = productSyncTypeFilter.value;
  const enabledFilter = productSyncEnabledFilter.value;
  const filteredSources = productSyncSources.filter((item) => {
    if (typeFilter && item.source_type !== typeFilter) {
      return false;
    }
    if (enabledFilter === "true" && !item.enabled) {
      return false;
    }
    if (enabledFilter === "false" && item.enabled) {
      return false;
    }
    return true;
  });

  const enabledCount = filteredSources.filter((item) => item.enabled).length;
  const fileCount = filteredSources.filter((item) => item.source_type === "file").length;
  const urlCount = filteredSources.filter((item) => item.source_type === "url").length;
  const successCount = filteredSources.filter((item) => item.last_status === "success").length;

  productSyncMetricGrid.innerHTML = "";
  const metrics = [
    ["同步来源数", filteredSources.length],
    ["已启用", enabledCount],
    ["文件来源", fileCount],
    ["URL 来源", urlCount],
    ["最近成功", successCount],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    productSyncMetricGrid.appendChild(card);
  });

  productSyncList.innerHTML = "";
  if (!filteredSources.length) {
    productSyncStatus.textContent = "当前筛选条件下没有同步来源";
    productSyncList.innerHTML = "<p class=\"analytics-empty\">还没有配置自动同步来源</p>";
    return;
  }

  productSyncStatus.textContent = `已加载 ${filteredSources.length} 个自动同步来源`;

  filteredSources.forEach((item) => {
    const row = productSyncRowTemplate.content.firstElementChild.cloneNode(true);
    row.querySelector(".trend-source-badge").textContent = item.source_id;
    row.querySelector(".trend-category-badge").textContent = item.source_type === "file" ? "文件" : "URL";
    row.querySelector(".trend-keyword").textContent = item.name;
    row.querySelector(".trend-score-badge").textContent = item.enabled ? "已启用" : "已停用";
    row.querySelector(".sales-score-badge").textContent = item.adapter || "自动识别";
    row.querySelector(".trend-product-link").textContent =
      `${item.location} · 最近导入 ${item.last_imported_count || 0} 个商品`;

    row.querySelector(".product-sync-edit-name").value = item.name || "";
    row.querySelector(".product-sync-edit-type").value = item.source_type || "file";
    row.querySelector(".product-sync-edit-location").value = item.location || "";
    row.querySelector(".product-sync-edit-adapter").value = item.adapter || "";
    row.querySelector(".product-sync-edit-enabled").value = item.enabled ? "true" : "false";
    row.querySelector(".product-sync-edit-notes").value = item.notes || "";

    const statusNode = row.querySelector(".trend-mapping-status");
    statusNode.textContent = item.last_synced_at
      ? `最近同步：${item.last_synced_at} · ${item.last_status || "未知"}${item.last_message ? ` · ${item.last_message}` : ""}`
      : "还没有执行过自动同步";

    const syncSaveBtn = row.querySelector(".product-sync-save-button");
    const syncRunBtn = row.querySelector(".product-sync-run-button");
    syncSaveBtn.addEventListener("click", () => {
      withButtonLoading(syncSaveBtn, "保存中...", () => saveProductSyncSource(item.source_id, row, statusNode));
    });
    syncRunBtn.addEventListener("click", () => {
      withButtonLoading(syncRunBtn, "同步中...", () => runProductSyncSource(item.source_id, statusNode));
    });

    makeRowCollapsible(row);
    productSyncList.appendChild(row);
  });
}

function renderProductManagement() {
  const sourceFilter = productManagementSourceFilter.value;
  const categoryFilter = productManagementCategoryFilter.value;
  const filteredProducts = productCatalog.filter((item) => {
    if (sourceFilter && item.source !== sourceFilter) {
      return false;
    }
    if (categoryFilter && item.category !== categoryFilter) {
      return false;
    }
    return true;
  });

  const manualCount = filteredProducts.filter((item) => item.source === "manual").length;
  const externalCount = filteredProducts.length - manualCount;
  const averagePrice = filteredProducts.length
    ? (filteredProducts.reduce((sum, item) => sum + Number(item.price || 0), 0) / filteredProducts.length).toFixed(1)
    : "0.0";
  const lowStockCount = filteredProducts.filter((item) => Number(item.stock || 0) < 20).length;

  productManagementMetricGrid.innerHTML = "";
  const metrics = [
    ["商品数", filteredProducts.length],
    ["手工商品", manualCount],
    ["外部来源商品", externalCount],
    ["平均价格", `¥${averagePrice}`],
    ["低库存(<20)", lowStockCount],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    productManagementMetricGrid.appendChild(card);
  });

  productManagementList.innerHTML = "";
  if (!filteredProducts.length) {
    productManagementStatus.textContent = "当前筛选条件下没有商品";
    productManagementList.innerHTML = "<p class=\"analytics-empty\">还没有匹配的商品记录</p>";
    return;
  }

  productManagementStatus.textContent = `已加载 ${filteredProducts.length} 个商品，可直接编辑并保存`;

  filteredProducts
    .slice()
    .sort((left, right) => left.title.localeCompare(right.title, "zh-CN"))
    .forEach((item) => {
      const row = productManagementRowTemplate.content.firstElementChild.cloneNode(true);
      row.querySelector(".trend-source-badge").textContent = item.source || "manual";
      row.querySelector(".trend-category-badge").textContent = item.category;
      row.querySelector(".trend-keyword").textContent = item.title;
      row.querySelector(".trend-score-badge").textContent = `热度 ${Number(item.popularity_score || 0).toFixed(1)}`;
      row.querySelector(".sales-score-badge").textContent = `销量 ${Number(item.sales_score || 0).toFixed(1)}`;
      row.querySelector(".trend-product-link").textContent =
        `${item.product_id} · ${item.brand} · ¥${item.price} · 库存 ${item.stock} · 评分 ${Number(item.rating || 0).toFixed(1)}`;

      row.querySelector(".product-edit-title").value = item.title || "";
      row.querySelector(".product-edit-category").value = item.category || "";
      row.querySelector(".product-edit-brand").value = item.brand || "";
      row.querySelector(".product-edit-price").value = item.price ?? "";
      row.querySelector(".product-edit-stock").value = item.stock ?? "";
      row.querySelector(".product-edit-rating").value = item.rating ?? "";
      row.querySelector(".product-edit-source").value = item.source || "";
      row.querySelector(".product-edit-external-id").value = item.external_id || "";
      row.querySelector(".product-edit-popularity").value = item.popularity_score ?? 0;
      row.querySelector(".product-edit-sales").value = item.sales_score ?? 0;
      row.querySelector(".product-edit-image-url").value = item.image_url || "";
      row.querySelector(".product-edit-features").value = (item.features || []).join(", ");
      row.querySelector(".product-edit-description").value = item.description || "";

      const statusNode = row.querySelector(".trend-mapping-status");
      statusNode.textContent = item.external_id
        ? `外部 ID：${item.external_id}`
        : "当前没有外部 ID";

      const productSaveBtn = row.querySelector(".product-save-button");
      productSaveBtn.addEventListener("click", () => {
        withButtonLoading(productSaveBtn, "保存中...", () => saveManagedProduct(item.product_id, row, statusNode));
      });

      makeRowCollapsible(row);
      productManagementList.appendChild(row);
    });
}

async function createManagedProduct() {
  const productId = productCreateIdInput.value.trim();
  const title = productCreateTitleInput.value.trim();
  const category = productCreateCategoryInput.value.trim();
  const brand = productCreateBrandInput.value.trim();
  const source = productCreateSourceInput.value.trim() || "manual";

  if (!productId || !title || !category || !brand) {
    productManagementStatus.textContent = "请至少填写商品 ID、标题、品类和品牌";
    return;
  }

  const payload = {
    product_id: productId,
    title,
    category,
    brand,
    price: Number(productCreatePriceInput.value || 0),
    description: productCreateDescriptionInput.value.trim() || `${title} 商品记录`,
    features: parseListInput(productCreateFeaturesInput.value),
    image_url: productCreateImageInput.value.trim() || "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
    stock: Math.max(0, Number(productCreateStockInput.value || 0)),
    rating: Number(productCreateRatingInput.value || 0),
    source,
    external_id: productCreateExternalIdInput.value.trim() || null,
    popularity_score: Math.max(0, Number(productCreatePopularityInput.value || 0)),
    sales_score: Math.max(0, Number(productCreateSalesInput.value || 0)),
  };

  productManagementStatus.textContent = "正在新增商品...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/products`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`新增商品失败 ${response.status}`);
    }

    await response.json();
    resetProductCreateForm();
    productManagementStatus.textContent = "已新增商品";
    loadProductSourceManagement();
  } catch (error) {
    productManagementStatus.textContent = `新增失败：${error.message}`;
  }
}

async function createProductSyncSource() {
  const sourceId = productSyncCreateIdInput.value.trim();
  const name = productSyncCreateNameInput.value.trim();
  const sourceType = productSyncCreateTypeInput.value;
  const location = productSyncCreateLocationInput.value.trim();

  if (!sourceId || !name || !location) {
    productSyncStatus.textContent = "请至少填写同步来源 ID、名称和位置";
    return;
  }

  const payload = {
    source_id: sourceId,
    name,
    source_type: sourceType,
    location,
    adapter: productSyncCreateAdapterSelect.value || null,
    enabled: productSyncCreateEnabledSelect.value === "true",
    notes: productSyncCreateNotesInput.value.trim() || null,
    last_imported_count: 0,
  };

  productSyncStatus.textContent = "正在新增自动同步来源...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-sync-sources`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`新增同步来源失败 ${response.status}`);
    }

    productSyncCreateForm.reset();
    productSyncCreateEnabledSelect.value = "true";
    productSyncStatus.textContent = "已新增自动同步来源";
    loadProductSyncManagement();
  } catch (error) {
    productSyncStatus.textContent = `新增失败：${error.message}`;
  }
}

async function saveManagedProduct(productId, row, statusNode) {
  const payload = {
    title: row.querySelector(".product-edit-title").value.trim(),
    category: row.querySelector(".product-edit-category").value.trim(),
    brand: row.querySelector(".product-edit-brand").value.trim(),
    price: Number(row.querySelector(".product-edit-price").value || 0),
    stock: Math.max(0, Number(row.querySelector(".product-edit-stock").value || 0)),
    rating: Number(row.querySelector(".product-edit-rating").value || 0),
    source: row.querySelector(".product-edit-source").value.trim() || "manual",
    external_id: row.querySelector(".product-edit-external-id").value.trim() || null,
    popularity_score: Math.max(0, Number(row.querySelector(".product-edit-popularity").value || 0)),
    sales_score: Math.max(0, Number(row.querySelector(".product-edit-sales").value || 0)),
    image_url: row.querySelector(".product-edit-image-url").value.trim() || "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
    features: parseListInput(row.querySelector(".product-edit-features").value),
    description: row.querySelector(".product-edit-description").value.trim(),
  };

  if (!payload.title || !payload.category || !payload.brand) {
    statusNode.textContent = "标题、品类和品牌不能为空";
    return;
  }

  statusNode.textContent = "正在保存商品...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/products/${encodeURIComponent(productId)}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`保存商品失败 ${response.status}`);
    }

    statusNode.textContent = "商品已保存";
    loadProductSourceManagement();
  } catch (error) {
    statusNode.textContent = `保存失败：${error.message}`;
  }
}

async function saveProductSyncSource(sourceId, row, statusNode) {
  const payload = {
    name: row.querySelector(".product-sync-edit-name").value.trim(),
    source_type: row.querySelector(".product-sync-edit-type").value,
    location: row.querySelector(".product-sync-edit-location").value.trim(),
    adapter: row.querySelector(".product-sync-edit-adapter").value.trim() || null,
    enabled: row.querySelector(".product-sync-edit-enabled").value === "true",
    notes: row.querySelector(".product-sync-edit-notes").value.trim() || null,
  };

  if (!payload.name || !payload.location) {
    statusNode.textContent = "名称和位置不能为空";
    return;
  }

  statusNode.textContent = "正在保存同步来源...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-sync-sources/${encodeURIComponent(sourceId)}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`保存同步来源失败 ${response.status}`);
    }

    statusNode.textContent = "同步来源已保存";
    loadProductSyncManagement();
  } catch (error) {
    statusNode.textContent = `保存失败：${error.message}`;
  }
}

async function runProductSyncSource(sourceId, statusNode) {
  statusNode.textContent = "正在执行同步...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-sync-sources/${encodeURIComponent(sourceId)}/run`, {
      method: "POST",
    });

    if (!response.ok) {
      throw new Error(`执行同步失败 ${response.status}`);
    }

    const payload = await response.json();
    statusNode.textContent = payload.status === "success"
      ? `同步完成：导入 ${payload.imported_count} 个商品`
      : `同步失败：${payload.message || "未知错误"}`;
    loadProductSourceManagement();
    loadProductSyncManagement();
    loadImportHistory();
  } catch (error) {
    statusNode.textContent = `同步失败：${error.message}`;
  }
}

async function runAllProductSyncSources() {
  productSyncStatus.textContent = "正在同步全部启用来源...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/product-sync-sources/run-all`, {
      method: "POST",
    });

    if (!response.ok) {
      throw new Error(`批量同步失败 ${response.status}`);
    }

    const payload = await response.json();
    productSyncStatus.textContent =
      `同步完成：共 ${payload.total_sources} 个来源，成功 ${payload.success_count}，失败 ${payload.error_count}`;
    loadProductSourceManagement();
    loadProductSyncManagement();
    loadImportHistory();
  } catch (error) {
    productSyncStatus.textContent = `同步失败：${error.message}`;
  }
}

async function buildProductImportDraft() {
  const selectedFile = productImportFileInput.files?.[0] || null;
  const manualContent = productImportContentInput.value.trim();
  const adapter = productImportAdapterSelect.value || null;

  let content = manualContent;
  let filename = manualContent.startsWith("[") ? "pasted_products.json" : "pasted_products.csv";

  if (selectedFile) {
    content = await selectedFile.text();
    filename = selectedFile.name;
  }

  if (!content.trim()) {
    return null;
  }

  return {
    content,
    filename,
    adapter,
  };
}

async function previewProductBatch() {
  const draft = await buildProductImportDraft();
  if (!draft) {
    productPreviewStatus.textContent = "请先选择文件，或者粘贴商品 JSON / CSV 内容";
    return;
  }

  productPreviewStatus.textContent = "正在生成商品导入预览...";
  productPreviewMetricGrid.innerHTML = "";
  productPreviewList.innerHTML = "";

  try {
    const response = await fetch(`${API_BASE_URL}/api/products/batch-preview`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(draft),
    });

    if (!response.ok) {
      let detail = `商品导入预览失败 ${response.status}`;
      try {
        const payload = await response.json();
        if (payload.detail) {
          detail = payload.detail;
        }
      } catch (error) {
        // ignore malformed error body
      }
      throw new Error(detail);
    }

    const payload = await response.json();
    renderProductImportPreview(payload);
    loadImportHistory();
  } catch (error) {
    productPreviewStatus.textContent = `预览失败：${error.message}`;
    loadImportHistory();
  }
}

function renderProductImportPreview(payload) {
  productPreviewStatus.textContent =
    `预览完成：共 ${payload.total_count} 条，${payload.ready_count} 条可导入，${payload.error_count} 条有问题，使用适配器 ${payload.adapter}`;

  renderProductPresetPanel(payload);

  productPreviewMetricGrid.innerHTML = "";
  const metrics = [
    ["总条数", payload.total_count],
    ["可导入", payload.ready_count],
    ["错误条数", payload.error_count],
    ["自动生成 ID", payload.generated_product_id_count],
  ];
  metrics.forEach(([label, value]) => {
    const card = metricTemplate.content.firstElementChild.cloneNode(true);
    card.querySelector(".metric-label").textContent = label;
    card.querySelector(".metric-value").textContent = value;
    productPreviewMetricGrid.appendChild(card);
  });

  productPreviewList.innerHTML = "";
  payload.items.forEach((item) => {
    const row = productPreviewRowTemplate.content.firstElementChild.cloneNode(true);
    const isReady = item.status === "ready";
    row.classList.toggle("is-error", !isReady);

    row.querySelector(".trend-preview-status-badge").textContent = isReady ? "可导入" : "有问题";
    row.querySelector(".trend-preview-status-badge").classList.toggle("is-error", !isReady);
    row.querySelector(".trend-preview-row-number").textContent = `第 ${item.row_number} 行`;
    row.querySelector(".trend-preview-keyword").textContent = item.title || "无法解析商品标题";
    row.querySelector(".trend-preview-trend-score").textContent =
      item.popularity_score !== null && item.popularity_score !== undefined
        ? `热度 ${Number(item.popularity_score).toFixed(1)}`
        : "热度 -";
    row.querySelector(".trend-preview-sales-score").textContent =
      item.sales_score !== null && item.sales_score !== undefined
        ? `销量 ${Number(item.sales_score).toFixed(1)}`
        : "销量 -";
    row.querySelector(".trend-preview-meta").textContent = item.source && item.category
      ? `${item.source} · ${item.category} · ${item.brand || "Unknown"}`
      : "该行字段不完整";
    row.querySelector(".trend-preview-detail").textContent = isReady
      ? buildProductPreviewDetail(item)
      : item.error || "该行存在无法导入的问题";

    productPreviewList.appendChild(row);
  });
}

function renderProductPresetPanel(payload) {
  const mappedHeaders = payload.mapped_headers || [];
  const unmappedHeaders = payload.unmapped_headers || [];
  const detectedHeaders = payload.detected_headers || [];

  const mappedMarkup = mappedHeaders.length
    ? mappedHeaders
        .map((item) => `<span class="preset-mapping-chip">${escapeHtml(item.source_field)} -> ${escapeHtml(item.target_field)}</span>`)
        .join("")
    : "<p class=\"preset-empty\">这次没有识别到可映射字段。</p>";

  const unmappedMarkup = unmappedHeaders.length
    ? unmappedHeaders
        .map((header) => `<span class="preset-unmapped-chip">${escapeHtml(header)}</span>`)
        .join("")
    : "<span class=\"preset-ok\">没有额外未识别字段</span>";

  const detectedMarkup = detectedHeaders.length
    ? detectedHeaders
        .map((header) => `<span class="preset-detected-chip">${escapeHtml(header)}</span>`)
        .join("")
    : "<span class=\"preset-empty\">当前内容里还没有可识别表头</span>";

  productPresetPanel.innerHTML = `
    <div class="preset-section">
      <p class="preset-label">识别到的平台模板</p>
      <strong class="preset-title">${escapeHtml(payload.adapter)}</strong>
      <p class="preset-description">${escapeHtml(payload.adapter_description || "未提供模板描述")}</p>
    </div>
    <div class="preset-section">
      <p class="preset-label">检测到的原始字段</p>
      <div class="preset-chip-list">${detectedMarkup}</div>
    </div>
    <div class="preset-section">
      <p class="preset-label">字段映射预设</p>
      <div class="preset-chip-list">${mappedMarkup}</div>
    </div>
    <div class="preset-section">
      <p class="preset-label">未使用字段</p>
      <div class="preset-chip-list">${unmappedMarkup}</div>
    </div>
  `;
}

function buildProductPreviewDetail(item) {
  const segments = [];
  if (item.generated_product_id) {
    segments.push(`自动生成商品 ID：${item.product_id}`);
  } else if (item.product_id) {
    segments.push(`商品 ID：${item.product_id}`);
  }

  if (item.external_id) {
    segments.push(`外部 ID：${item.external_id}`);
  }

  if (item.price !== null && item.price !== undefined) {
    segments.push(`价格：¥${item.price}`);
  }

  if (item.stock !== null && item.stock !== undefined) {
    segments.push(`库存：${item.stock}`);
  }

  return segments.join(" · ");
}

function clearProductPreview() {
  productPreviewStatus.textContent = "点击“先预览商品导入”后，这里会显示商品条数、错误行和自动生成的商品 ID。";
  productPresetPanel.innerHTML = "";
  productPreviewMetricGrid.innerHTML = "";
  productPreviewList.innerHTML = "";
}

async function importProductBatch() {
  const draft = await buildProductImportDraft();
  if (!draft) {
    productImportStatus.textContent = "请先选择文件，或者粘贴商品 JSON / CSV 内容";
    return;
  }

  productImportStatus.textContent = "正在批量导入商品...";

  try {
    const response = await fetch(`${API_BASE_URL}/api/products/batch-import`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(draft),
    });

    if (!response.ok) {
      let detail = `商品批量导入失败 ${response.status}`;
      try {
        const payload = await response.json();
        if (payload.detail) {
          detail = payload.detail;
        }
      } catch (error) {
        // ignore malformed error body
      }
      throw new Error(detail);
    }

    const payload = await response.json();
    productImportStatus.textContent =
      `已导入 ${payload.imported_count} 个商品，自动生成 ${payload.generated_product_id_count} 个商品 ID，使用适配器 ${payload.adapter}`;
    productImportForm.reset();
    clearProductPreview();
    loadProductSourceManagement();
    loadTrendManagement();
    loadImportHistory();
  } catch (error) {
    productImportStatus.textContent = `导入失败：${error.message}`;
    loadImportHistory();
  }
}

function buildNewTrendId(source, keyword, category) {
  const timestamp = Date.now().toString(36);
  return slugify(`${source}_${category}_${keyword}_${timestamp}`);
}

function slugify(value) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^0-9a-z\u4e00-\u9fff]+/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_|_$/g, "") || "trend_item";
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function resetTrendCreateForm(previousSource, previousCategory) {
  trendCreateForm.reset();
  trendCreateSourceInput.value = previousSource;
  trendCreateCategoryInput.value = previousCategory;
  trendCreateProductSelect.value = "";
}

function resetProductCreateForm() {
  productCreateForm.reset();
  productCreateSourceInput.value = "manual";
}

function resetDirectionCreateForm() {
  directionCreateForm.reset();
  buildDirectionProductSelector(directionCreateProductSelector, [], productCatalog);
}

function setStatus(message, isError) {
  statusText.textContent = message;
  statusText.classList.toggle("is-error", isError);
}

function parseListInput(value) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function makeRowCollapsible(row) {
  row.classList.add("is-collapsed");
  const head = row.querySelector(".trend-row-head");
  if (!head) return;

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "row-toggle-btn";
  toggle.setAttribute("aria-label", "展开编辑");
  const scoresDiv = head.querySelector(".trend-scores");
  if (scoresDiv) {
    scoresDiv.after(toggle);
  } else {
    head.appendChild(toggle);
  }

  head.addEventListener("click", (e) => {
    if (e.target.closest("button:not(.row-toggle-btn), select, input, a")) return;
    const nowCollapsed = row.classList.toggle("is-collapsed");
    toggle.setAttribute("aria-label", nowCollapsed ? "展开编辑" : "收起");
  });
}

function buildDirectionProductSelector(container, initialLinks, products) {
  const state = initialLinks.map((link) => ({
    product_id: link.product_id,
    product_role: link.product_role || "推荐商品",
  }));
  rerenderDirectionSelector(container, state, products);
}

function rerenderDirectionSelector(container, state, products) {
  container.innerHTML = "";
  const sortedProducts = [...products].sort((left, right) => left.title.localeCompare(right.title, "zh-CN"));
  const selectedIds = new Set(state.map((entry) => entry.product_id));

  state.forEach((entry, index) => {
    const matched = products.find((product) => product.product_id === entry.product_id);
    const row = document.createElement("div");
    row.className = "direction-selector-row";
    row.dataset.productId = entry.product_id;
    row.dataset.productRole = entry.product_role;

    const roleSelect = document.createElement("select");
    roleSelect.className = "direction-selector-role";
    DIRECTION_ROLES.forEach((role) => {
      const opt = document.createElement("option");
      opt.value = role;
      opt.textContent = role;
      if (role === entry.product_role) opt.selected = true;
      roleSelect.appendChild(opt);
    });
    roleSelect.addEventListener("change", () => {
      row.dataset.productRole = roleSelect.value;
    });

    const nameSpan = document.createElement("span");
    nameSpan.className = "direction-selector-product-name";
    nameSpan.textContent = matched ? `${matched.title}` : entry.product_id;
    nameSpan.title = entry.product_id;

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "direction-selector-remove";
    removeBtn.textContent = "×";
    removeBtn.addEventListener("click", () => {
      const nextState = state.filter((_, i) => i !== index);
      rerenderDirectionSelector(container, nextState, products);
    });

    row.appendChild(roleSelect);
    row.appendChild(nameSpan);
    row.appendChild(removeBtn);
    container.appendChild(row);
  });

  const addRow = document.createElement("div");
  addRow.className = "direction-selector-add-row";

  const productSelect = document.createElement("select");
  productSelect.className = "direction-selector-product-select";
  const emptyOpt = document.createElement("option");
  emptyOpt.value = "";
  emptyOpt.textContent = "添加商品...";
  productSelect.appendChild(emptyOpt);
  sortedProducts.forEach((product) => {
    if (selectedIds.has(product.product_id)) return;
    const opt = document.createElement("option");
    opt.value = product.product_id;
    opt.textContent = `${product.title} (${product.product_id})`;
    productSelect.appendChild(opt);
  });

  const addRoleSelect = document.createElement("select");
  addRoleSelect.className = "direction-selector-add-role";
  DIRECTION_ROLES.forEach((role) => {
    const opt = document.createElement("option");
    opt.value = role;
    opt.textContent = role;
    addRoleSelect.appendChild(opt);
  });

  const addBtn = document.createElement("button");
  addBtn.type = "button";
  addBtn.className = "direction-selector-add-btn";
  addBtn.textContent = "+ 添加";
  addBtn.addEventListener("click", () => {
    const productId = productSelect.value;
    if (!productId) return;
    const nextState = [...state, { product_id: productId, product_role: addRoleSelect.value }];
    rerenderDirectionSelector(container, nextState, products);
  });

  addRow.appendChild(productSelect);
  addRow.appendChild(addRoleSelect);
  addRow.appendChild(addBtn);
  container.appendChild(addRow);
}

function readDirectionProductSelector(container, directionId) {
  return Array.from(container.querySelectorAll(".direction-selector-row"))
    .map((row, index) => ({
      direction_id: directionId,
      product_id: row.dataset.productId,
      product_role: row.dataset.productRole,
      priority: index + 1,
    }))
    .filter((link) => link.product_id);
}

function buildDirectionLinksFromInput(directionId, rawValue) {
  return parseListInput(rawValue)
    .map((item, index) => {
      const [productIdPart, rolePart] = item.split(":");
      const productId = (productIdPart || "").trim();
      const productRole = (rolePart || "").trim() || defaultDirectionRole(index);
      if (!productId) {
        return null;
      }
      return {
        direction_id: directionId,
        product_id: productId,
        product_role: productRole,
        priority: index + 1,
      };
    })
    .filter(Boolean);
}

function getDirectionLinks(directionId) {
  return directionProductLinks
    .filter((link) => link.direction_id === directionId)
    .slice()
    .sort((left, right) => Number(left.priority || 0) - Number(right.priority || 0));
}

function buildDirectionLinkLabel(link) {
  const matchedProduct = productCatalog.find((item) => item.product_id === link.product_id);
  if (matchedProduct) {
    return `${matchedProduct.title}(${link.product_role})`;
  }
  return `${link.product_id}(${link.product_role})`;
}

function formatDirectionLinksForInput(links) {
  return links.map((link) => `${link.product_id}:${link.product_role}`).join(", ");
}

function defaultDirectionRole(index) {
  if (index === 0) {
    return "核心商品";
  }
  if (index === 1) {
    return "入门款";
  }
  return "推荐商品";
}

function buildDirectionRoleCopy(role, count) {
  if (role === "入门款") {
    return `这一层更适合第一次进入该方向的用户，现在有 ${count} 个可选商品。`;
  }
  if (role === "核心商品") {
    return `这是当前方向最关键的一层，优先围绕这 ${count} 个商品做决策会更稳。`;
  }
  if (role === "进阶款") {
    return `当用户已经明确方向、想继续升级时，可以重点看这 ${count} 个商品。`;
  }
  if (role === "搭配款") {
    return `这层更适合补齐配置或提升体验，现在整理了 ${count} 个搭配商品。`;
  }
  if (role === "替代款") {
    return `如果预算、品牌或风格有变化，这里有 ${count} 个替代选择可以横向比较。`;
  }
  return `这一层当前整理了 ${count} 个商品，可以作为该方向的补充参考。`;
}

function directionRoleRank(role) {
  const rankMap = {
    "核心商品": 0,
    "入门款": 1,
    "进阶款": 2,
    "搭配款": 3,
    "替代款": 4,
    "推荐商品": 5,
  };
  return rankMap[role] ?? 99;
}

function parseNumberInput(value) {
  const number = Number(value);
  return Number.isFinite(number) && number > 0 ? number : null;
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function sourceLabel(source) {
  if (source === "itemcf") {
    return "行为相似推荐";
  }

  return "画像规则推荐";
}

function explanationLabel(provider) {
  if (provider === "openai") {
    return "LLM解释";
  }

  if (provider && provider.includes("fallback")) {
    return "模板兜底";
  }

  return "模板解释";
}

function parseStageHash() {
  const rawHash = window.location.hash || "#directions";
  const [path, queryString] = rawHash.split("?");
  const params = new URLSearchParams(queryString || "");

  if (path.startsWith("#admin")) {
    return { page: "admin", directionId: "", directionTitle: "" };
  }

  return {
    page: path === "#products" ? "products" : "directions",
    directionId: params.get("direction_id") || "",
    directionTitle: params.get("direction_title") || "",
  };
}

function buildProductStageHash(directionId = "", directionTitle = "") {
  const params = new URLSearchParams();
  if (directionId) {
    params.set("direction_id", directionId);
  }
  if (directionTitle) {
    params.set("direction_title", directionTitle);
  }

  const query = params.toString();
  return query ? `#products?${query}` : "#products";
}

function isProductRoute() {
  return parseStageHash().page === "products";
}

function navigateToProductStage(directionId = "", directionTitle = "") {
  const targetHash = buildProductStageHash(directionId, directionTitle);
  if (window.location.hash === targetHash) {
    syncStageFromHash();
    return;
  }

  window.location.hash = targetHash;
}

function navigateToDirectionStage() {
  if (window.location.hash === "#directions" || window.location.hash === "") {
    syncStageFromHash();
    return;
  }

  window.location.hash = "#directions";
}

function renderProductStageHeader() {
  if (selectedDirectionId && selectedDirectionTitle) {
    productStageTitle.textContent = `${selectedDirectionTitle} · 商品推荐`;
    productStageIntro.textContent = "系统会先锁定这个方向，再在该方向下返回更具体的商品建议。";
    activeDirectionText.textContent = `当前方向：${selectedDirectionTitle}`;
    activeDirectionBanner.classList.remove("is-hidden");
    renderDirectionLayerPanel();
    return;
  }

  productStageTitle.textContent = "商品推荐页";
  productStageIntro.textContent = "这里会根据当前用户和推荐场景，返回更具体的商品建议。";
  activeDirectionText.textContent = "";
  activeDirectionBanner.classList.add("is-hidden");
  directionLayerPanel.classList.add("is-hidden");
  directionLayerStatus.textContent = "这里会按入门款、核心商品、搭配款等层次展示当前方向的商品结构。";
  directionLayerGrid.innerHTML = "";
}

function renderDirectionLayerPanel() {
  if (!selectedDirectionId) {
    directionLayerPanel.classList.add("is-hidden");
    directionLayerGrid.innerHTML = "";
    return;
  }

  const links = getDirectionLinks(selectedDirectionId);
  if (!links.length) {
    directionLayerPanel.classList.add("is-hidden");
    directionLayerGrid.innerHTML = "";
    return;
  }

  const grouped = links.reduce((accumulator, link) => {
    const role = link.product_role || "推荐商品";
    accumulator[role] = accumulator[role] || [];
    accumulator[role].push(link);
    return accumulator;
  }, {});

  directionLayerPanel.classList.remove("is-hidden");
  directionLayerStatus.textContent = `当前方向共 ${links.length} 个商品，已经按角色分层整理。`;
  directionLayerGrid.innerHTML = "";

  Object.entries(grouped)
    .sort(([leftRole], [rightRole]) => directionRoleRank(leftRole) - directionRoleRank(rightRole))
    .forEach(([role, roleLinks]) => {
      const card = document.createElement("article");
      card.className = "direction-layer-card";

      const title = document.createElement("h4");
      title.className = "direction-layer-role";
      title.textContent = role;
      card.appendChild(title);

      const copy = document.createElement("p");
      copy.className = "direction-layer-copy";
      copy.textContent = buildDirectionRoleCopy(role, roleLinks.length);
      card.appendChild(copy);

      const items = document.createElement("div");
      items.className = "direction-layer-items";

      roleLinks.forEach((link) => {
        const item = document.createElement("span");
        item.className = "direction-layer-item";
        const matchedProduct = productCatalog.find((product) => product.product_id === link.product_id);
        item.textContent = matchedProduct ? `${matchedProduct.title} · ¥${matchedProduct.price}` : link.product_id;
        items.appendChild(item);
      });

      card.appendChild(items);
      directionLayerGrid.appendChild(card);
    });
}

function syncStageFromHash() {
  const route = parseStageHash();

  if (route.page === "admin") {
    userView.classList.add("is-hidden");
    adminView.classList.remove("is-hidden");
    navTabUser.classList.remove("is-active");
    navTabAdmin.classList.add("is-active");
    headerUserSelect.classList.add("is-hidden");
    return;
  }

  userView.classList.remove("is-hidden");
  adminView.classList.add("is-hidden");
  navTabUser.classList.add("is-active");
  navTabAdmin.classList.remove("is-active");
  headerUserSelect.classList.remove("is-hidden");

  if (route.page === "products") {
    selectedDirectionId = route.directionId;
    selectedDirectionTitle = route.directionTitle;
    renderProductStageHeader();
    directionStage.classList.add("is-hidden");
    productStage.classList.remove("is-hidden");
    loadRecommendations();
    productStage.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }

  selectedDirectionId = "";
  selectedDirectionTitle = "";
  renderProductStageHeader();
  productStage.classList.add("is-hidden");
  directionStage.classList.remove("is-hidden");

  if (!directionGrid.children.length) {
    if (activeDirectionMode === "user") {
      loadDirectionRecommendationsForUser();
    } else {
      loadDirectionRecommendationsForCategory();
    }
  }
}

setDirectionMode(activeDirectionMode, { autoLoad: false });
resetProductCreateForm();
productSyncCreateEnabledSelect.value = "true";
loadAnalytics();
loadTrendManagement();
loadProductSourceManagement();
loadProductSyncManagement();
loadUserManagement();
loadDirectionManagement();
loadImportHistory();
syncStageFromHash();
