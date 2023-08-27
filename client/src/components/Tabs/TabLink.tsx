interface Props {
  name: string;
  currentTab: string;
  setCurrentTab: (tab: string) => void;
}

/**
 * Component used to change tabs on the main page
 */
function TabLink({ name, currentTab, setCurrentTab }: Props) {
  const tabClasses = ['tab-link'];
  if (currentTab === name) {
    tabClasses.push('active');
  }

  return (
    <button
      className={tabClasses.join(' ')}
      onClick={() => setCurrentTab(name)}
      type="button"
    >
      {name}
    </button>
  );
}

export default TabLink;
