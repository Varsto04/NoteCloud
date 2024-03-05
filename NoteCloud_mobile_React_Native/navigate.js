import React from "react";
import Main from "./components/Main"
import WorkPlace from "./components/WorkPlace";
import Account from "./components/Account";
import GlobalAccess from "./components/GlobalAccess";

import { createStackNavigator } from "@react-navigation/stack";
import { NavigationContainer } from "@react-navigation/native";

const Stack = createStackNavigator();

export default function Navigate() {
    return <NavigationContainer>
        <Stack.Navigator>
        {/* screenOptions={{ headerShown: false,}}> */}
            
            <Stack.Screen
                name = "Main"
                component={Main}
                options={{title: 'Main', headerShown: false}}/>
            
            <Stack.Screen
                name = "WorkPlace"
                component={WorkPlace}
                option={{title: 'WorkPlace'}}/>
            
            <Stack.Screen
                name = "Account"
                component={Account}
                option={{title: 'Account'}}/>

            <Stack.Screen
                name = "GlobalAcess"
                component={GlobalAccess}
                option={{title: 'GlobalAcess'}}/>
            
        </Stack.Navigator>
    </NavigationContainer>;
}

  