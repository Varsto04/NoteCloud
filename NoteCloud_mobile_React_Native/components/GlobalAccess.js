import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, Button, Platform, ScrollView, BackHandler, TouchableOpacity, Image, SafeAreaView} from 'react-native';

import * as SQLite from 'expo-sqlite';
import { useState, useEffect } from 'react';

export default function GlobalAccess({ navigation }) {
    const [db, setDb] = useState(SQLite.openDatabase('example.db'));
    const [user1_id,setUser1_id] = useState(undefined);
    const [user2_id,setUser2_id] = useState(undefined);
    const [user3_id,setUser3_id] = useState(undefined);
    const [isLoading, setIsLoading] = useState(true);
    const [notes, setNotes] = useState([]);

    useEffect(
        () => {
        setIsLoading(true)
        db.transaction(tx => {
          tx.executeSql('SELECT * FROM notes WHERE editable = 1', null,
          (txObj, resultSet) => (
            console.log(resultSet.rows._array),
            setUser1_id(JSON.stringify(resultSet.rows._array[0].user1_id)),
            setUser2_id(JSON.stringify(resultSet.rows._array[0].user2_id)),
            setUser3_id(JSON.stringify(resultSet.rows._array[0].user3_id)),
            setNotes(resultSet.rows._array),
            setIsLoading(false)
          ),
          (txObj, error) => console.log(error))
        });
      },
      [db]);


    function update(){
      console.log('update')
      setIsLoading(true)
      db.transaction(tx => {
        tx.executeSql('SELECT * FROM notes WHERE editable = 1', null,
        (txObj, resultSet) => (
          console.log(resultSet.rows._array),
          setUser1_id(JSON.stringify(resultSet.rows._array[0].user1_id)),
          setUser2_id(JSON.stringify(resultSet.rows._array[0].user2_id)),
          setUser3_id(JSON.stringify(resultSet.rows._array[0].user3_id)),
          setNotes(resultSet.rows._array),
          setIsLoading(false)
        ),
        (txObj, error) => console.log(error))
      });
    }

    const set_db_user_id = (old_user_id, new_user_id) => {
      console.log(old_user_id, new_user_id)
      if (new_user_id == ''){
        console.log('IF')
        db.transaction(tx => {
          tx.executeSql(`UPDATE notes SET ${old_user_id} = ?, content_user1 = null WHERE editable = 1`, [null]
          );
        });
      }
      else{
      console.log('ELSE')
      db.transaction(tx => {
        tx.executeSql(`UPDATE notes SET ${old_user_id} = ?, content_user1 = null WHERE editable = 1`, [new_user_id]
        );
      });}
      (update())
    }

    if (isLoading) {
    return (
        <SafeAreaView style={styles.loading}>
        <Text>Loading...</Text>
        </SafeAreaView>
    );
    }
    
    return (
        <SafeAreaView  style={styles.container}>
        <StatusBar animated = {true} hidden = {true} />
        {/* NOTES [{}] */}
        {/* <Text>{JSON.stringify(notes)}</Text> */}
        
        <View style={styles.row}>
          <TextInput fontSize = {30} editable multiline placeholder={'id'} defaultValue = {user1_id} onChangeText={setUser1_id} />
          {(user1_id != JSON.stringify(notes[0].user1_id) && user1_id != undefined)?
          <TouchableOpacity style={{borderWidth: 1,paddingVertical: 1,paddingHorizontal: 1,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
          onPress={()=>set_db_user_id('user1_id',user1_id)}>
            <Image source={require('../assets/check.png')} style={styles.square_button}/>
          </TouchableOpacity>:null}
          {/* <Text>new={user1_id} old={JSON.stringify(notes[0].user1_id)}</Text> */}
        </View>

        <View style={styles.row}>
          <TextInput fontSize = {30} editable multiline placeholder={'id'} defaultValue = {user2_id} onChangeText={setUser2_id} />
          {(user2_id != JSON.stringify(notes[0].user2_id) && user2_id != undefined)?
          <TouchableOpacity style={{borderWidth: 1,paddingVertical: 1,paddingHorizontal: 1,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
          onPress={()=>set_db_user_id('user2_id',user2_id)}>
            <Image source={require('../assets/check.png')} style={styles.square_button}/>
          </TouchableOpacity>:null}
          {/* <Text>new={user2_id} old={JSON.stringify(notes[0].user2_id)}</Text> */}
        </View>

        <View style={styles.row}>
          <TextInput fontSize = {30} editable multiline placeholder={'id'} defaultValue = {user3_id} onChangeText={setUser3_id} />
          {(user3_id != JSON.stringify(notes[0].user3_id) && user3_id != undefined)?
          <TouchableOpacity style={{borderWidth: 1,paddingVertical: 1,paddingHorizontal: 1,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
          onPress={()=>set_db_user_id('user3_id',user3_id)}>
            <Image source={require('../assets/check.png')} style={styles.square_button}/>
          </TouchableOpacity>:null}
          {/* <Text>new={user3_id} old={JSON.stringify(notes[0].user3_id)}</Text> */}
        </View>
        </SafeAreaView>
    )
}

// STYLES
const styles = StyleSheet.create({
  
    container: {
      flex: 1,
      backgroundColor: '#fff',
    },
    
    loading: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    
    row: {
      flexDirection: 'row',
      // alignItems: 'center',
      alignSelf: 'stretch',
      justifyContent: 'space-between',
      margin: 4,
      padding: 8,
    },
  
    
    textup: {
      flex: 0.9,
      fontSize: 30,
    },
  
    textdown: {
      flex: 0.9,
      fontSize: 20,
    },
  
    square_button: {
      height:30,
      width:30,
      margin: 8
    }
  
  });
  