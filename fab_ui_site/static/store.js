let store = {
  configCache: {
    users: [],
    projects: [],
  },
  searchResult: [],
};

messageCenter.subscribe(kUserListLoaded.id, ((st, data) => 
{
  st.configCache.users = data;
}).bind(this, store), store);

messageCenter.subscribe(kProjectsLoaded.id, ((st, data) =>
{
  st.configCache.projects = data;
}).bind(this, store), store);

messageCenter.subscribe(kSearchUpdated.id, ((st, data) => {
  st.searchResult = data;
}).bind(this, store), store);
