import { registerRootComponent } from 'expo';

import App from './App';

// registerRootComponent calls AppRegistry.registerComponent('main', () => App);
// ensures that whether app is loaded in Expo Go or in a native build, the environment is set up appropriately
registerRootComponent(App);
