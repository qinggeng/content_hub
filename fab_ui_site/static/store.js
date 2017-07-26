let store = {
  configCache: {
    users: defaultConfig.users,
    projects: defaultConfig.projects,
    priority: defaultConfig.priority,
    severity: defaultConfig.severity,
    status: defaultConfig.status,
  },
  searchResult: extend(defaultSearchResult),
  originalSearchResult: extend(defaultSearchResult),
};

messageCenter.subscribe(kUserListLoaded.id, ((st, data) => 
{
  st.configCache.users = data;
}).bind(this, store), store);

messageCenter.subscribe(kProjectsLoaded.id, ((st, data) =>
{
  st.configCache.projects = data;
}).bind(this, store), store);

messageCenter.subscribe(kPriorityLoaded.id, ((st, data) =>
{
  st.configCache.priority = data;
}).bind(this, store), store);

messageCenter.subscribe(kStatusLoaded.id, ((st, data) =>
{
  st.configCache.status = data;
}).bind(this, store), store);

messageCenter.subscribe(kSeverityLoaded.id, ((st, data) =>
{
  st.configCache.severity = data;
}).bind(this, store), store);

messageCenter.subscribe(kSearchUpdated.id, ((st, data) => {
  st.searchResult = data;
  st.originalSearchResult = extend(data, {});
  console.log(j2s(data));
  messageCenter.publish({
    type: kSearchResultUpdated.id,
    payload: {},
  });
}).bind(this, store), store);
