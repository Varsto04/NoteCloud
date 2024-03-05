import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, Button, Platform, ScrollView, BackHandler, TouchableOpacity, Image, SafeAreaView, Alert} from 'react-native';

import * as SQLite from 'expo-sqlite';
import { useState, useEffect } from 'react';


export default function WorkPlace({ navigation }) {
  const [db, setDb] = useState(SQLite.openDatabase('example.db'));
  const [notes, setNotes] = useState([]);
  const [currentNote, setCurrentNote] = useState(undefined);
  const [user_id, setUser_id] = useState(undefined)
  const [currentContent, setCurrentContent] = useState(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(()=>{
    db.transaction(tx => {
      tx.executeSql('SELECT * FROM notes WHERE editable = 1', null,
        (txObj, resultSet) => (setNotes(resultSet.rows._array)),
        (txObj, error) => console.log(error)
      );
    });
    db.transaction(tx => {
      tx.executeSql(`SELECT * FROM logins where id = 1`, null,
      (txObj, resultSet) => (setUser_id(resultSet.rows._array[0].user_id)),
      (txObj, error) => console.log(error)
      );
    });
    
  })
  

// MAIN PART

  const updateNote = () => {
    db.transaction(tx => {
      tx.executeSql('UPDATE notes SET note = ? WHERE editable = 1', [currentNote]
      );
    });
  };


  const updateContent = (content, currentContent) => {
    db.transaction(tx => {
      tx.executeSql(`UPDATE notes SET ${content} = ? WHERE editable = 1`, [currentContent]
      );
    });
  };

// INSERT UPDATE TO USEEFFECT()
  const update = () => {db.transaction(tx => {
    tx.executeSql('SELECT * FROM notes WHERE editable = 1', null,
      (txObj, resultSet) => (setNotes(resultSet.rows._array)),
      (txObj, error) => console.log(error)
    );
  });};

  const select_id = () => {
    db.transaction(tx => {
      tx.executeSql(`SELECT * FROM logins where id = 1`, null,
      (txObj, resultSet) => (setUser_id(JSON.stringify(resultSet.rows._array[0].user_id))),
      (txObj, error) => console.log(error)
      );
    });
  }

// CLOUD
  const send_data = () => {
    db.transaction(tx => {
    tx.executeSql('SELECT login,jwt_token FROM logins', null,
      (txObj, resultSet) => (get_csrf_token(resultSet.rows._array[0].login,resultSet.rows._array[0].jwt_token)),
      (txObj, error) => console.log(error));
    });
  };

  const get_csrf_token = (login, jwt_token) => {
    fetch('http://192.168.45.14:8000/mobile/get_csrf_token', { 
      method: 'GET', 
      credentials: 'include'  
    }) 
    .then(response => response.json()) 
    .then(data => {sendUpdateToServer(data.csrf_token, login, jwt_token);
    });
  };

  const sendUpdateToServer = (token, login, jwt_token) => {
    fetch('http://192.168.45.14:8000/mobile/save_cloud_note', { 
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json', 
        'X-CSRFToken': token
      }, 
      credentials: 'include',
      body: JSON.stringify({'login':login, 'jwt_token':jwt_token, 'data': notes})
    }) 
    .then(response => response.json()) 
    .then(data => {console.log("note send, recieve: ",data)}) //contains(notes,data.data) insert_data(data.data)
  };
// CLOUD


  const global_access = () => {
    if (JSON.stringify(notes[0].user_id) === "-1"){return <Text>It`s offline note</Text>}
    else{return <View style={{flexDirection: 'row',
    // alignItems: 'center',
    alignSelf: 'stretch',
    justifyContent: 'space-around',
    margin: 4,
    padding: 8,}}>
    
    <TouchableOpacity style={{fontSize: 20, marginTop: 10,borderWidth: 1,paddingVertical: 10,paddingHorizontal: 20,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}} onPress={send_data}>
    <Text style={{color:'#fff'}}>Send note</Text>
    </TouchableOpacity>

    <TouchableOpacity style={{fontSize: 20, marginTop: 10,borderWidth: 1,paddingVertical: 10,paddingHorizontal: 20,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}} onPress={()=>navigation.navigate('GlobalAcess')}>
    <Text style={{color:'#fff'}}> Access  </Text>
    </TouchableOpacity>
    
    <TouchableOpacity style={{fontSize: 20, marginTop: 10,borderWidth: 1,paddingVertical: 10,paddingHorizontal: 20,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}} onPress={()=>Alert.alert('Delete from Cloud', 'Are you sure you want to delete from the cloud? Access to the note will be lost.',[
      {text: 'Cancel',onPress: () => console.log('Cancel Pressed'),},
      {text: 'OK', onPress: () => console.log('OK Pressed')},])}>
    <Text style={{color:'#fff'}}>Delete ☁️</Text>
    </TouchableOpacity>

    </View>};
  };


  // RETURN
  const showAsUser_id = () => {
    {update()}
    return notes.map((note, index) => {
      return (
        <View key={index}>
        {/* <Text>User_id</Text> */}
        {global_access()}
          <View style={styles.row}>
            <TextInput maxLength={20} style={styles.textup} editable placeholder={note.note} defaultValue = {note.note} onChangeText={setCurrentNote}/>
            
            <View style={styles.row}>
            {(currentNote != undefined && currentNote != note.note && currentNote != '')?
            <TouchableOpacity style={{fontSize: 20,borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
            onPress={updateNote}>
              <Image source={require('../assets/header.png')} style={styles.square_button}/>
            </TouchableOpacity>:null}

            {(currentContent != undefined && currentContent != note.content)? 
            <TouchableOpacity style={{fontSize: 20,borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
            onPress={()=>{updateContent('content', currentContent)}}>
              <Image source={require('../assets/save.png')} style={styles.square_button}/>
            </TouchableOpacity>:null}
            </View>
          </View>

          <ScrollView style={{marginLeft:10,marginRight:10}}>
            <View>
              {/* <Text style={styles.textup}>{note.user_id}</Text> */}
              <TextInput style={styles.textdown} editable multiline placeholder={'Content...'} defaultValue = {note.content} onChangeText={setCurrentContent} />
              <Text style={styles.textup}>{note.user1_id}</Text>
              <Text style={styles.textdown}>{note.content_user1}</Text>
              <Text style={styles.textup}>{note.user2_id}</Text>
              <Text style={styles.textdown}>{note.content_user2}</Text>
              <Text style={styles.textup}>{note.user3_id}</Text>
              <Text style={styles.textdown}>{note.content_user3}</Text>
            </View>
          </ScrollView>

        </View>
      );
    });
  };

  const showAsUser1_id = () => {
    {update()}
    return notes.map((note, index) => {
      return (
        <View key={index}>
        {/* <Text>User1_id</Text> */}
          <View style={styles.row}>
            <TextInput maxLength={20} style={styles.textup} editable placeholder={note.note} defaultValue = {note.note} onChangeText={setCurrentNote}/>
            {global_access()}
            <View style={styles.row}>
            {(currentNote != undefined && currentNote != note.note && currentNote != '')?
            <TouchableOpacity style={{fontSize: 20,borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
            onPress={updateNote}>
              <Image source={require('../assets/header.png')} style={styles.square_button}/>
            </TouchableOpacity>:null}

            {(currentContent != undefined && currentContent != note.content)? 
            <TouchableOpacity style={{fontSize: 20,borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
            onPress={()=>{updateContent('content', currentContent)}}>
              <Image source={require('../assets/save.png')} style={styles.square_button}/>
            </TouchableOpacity>:null}
            </View>
          </View>

          <ScrollView style={{marginLeft:10,marginRight:10}}>
            <View>
              {/* <Text style={styles.textup}>{note.user1_id}</Text> */}
              <TextInput style={styles.textdown} editable multiline placeholder={'Content...'} defaultValue = {note.content_user1} onChangeText={setCurrentContent} />
              <Text style={styles.textup}>{note.user_id}</Text>
              <Text style={styles.textdown}>{note.content}</Text>
              <Text style={styles.textup}>{note.user2_id}</Text>
              <Text style={styles.textdown}>{note.content_user2}</Text>
              <Text style={styles.textup}>{note.user3_id}</Text>
              <Text style={styles.textdown}>{note.content_user3}</Text>
            </View>
          </ScrollView>

        </View>
      );
    });
  };

  const showAsUser2_id = () => {
    {update()}
    return notes.map((note, index) => {
      return (
        <View key={index}>
        {/* <Text>User2_id</Text> */}
          <View style={styles.row}>
            <TextInput maxLength={20} style={styles.textup} editable placeholder={note.note} defaultValue = {note.note} onChangeText={setCurrentNote}/>
            {global_access()}
            
            <View style={styles.row}>
            {(currentNote != undefined && currentNote != note.note && currentNote != '')?
            <TouchableOpacity style={{fontSize: 20,borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
            onPress={updateNote}>
              <Image source={require('../assets/header.png')} style={styles.square_button}/>
            </TouchableOpacity>:null}

            {(currentContent != undefined && currentContent != note.content)? 
            <TouchableOpacity style={{fontSize: 20,borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
            onPress={()=>{updateContent('content', currentContent)}}>
              <Image source={require('../assets/save.png')} style={styles.square_button}/>
            </TouchableOpacity>:null}
            </View>
          </View>

          <ScrollView style={{marginLeft:10,marginRight:10}}>
            <View>
              {/* <Text style={styles.textup}>{note.user2_id}</Text> */}
              <TextInput style={styles.textdown} editable multiline placeholder={'Content...'} defaultValue = {note.content_user2} onChangeText={setCurrentContent} />
              <Text style={styles.textup}>{note.user_id}</Text>
              <Text style={styles.textdown}>{note.content}</Text>
              <Text style={styles.textup}>{note.user1_id}</Text>
              <Text style={styles.textdown}>{note.content_user1}</Text>
              <Text style={styles.textup}>{note.user3_id}</Text>
              <Text style={styles.textdown}>{note.content_user3}</Text>
            </View>
          </ScrollView>

        </View>
      );
    });
  };
  
  const showAsUser3_id = () => {
    {update()}
    return notes.map((note, index) => {
      return (
        <View key={index}>
        {/* <Text>User3_id</Text> */}
          <View style={styles.row}>
            <TextInput maxLength={20} style={styles.textup} editable placeholder={note.note} defaultValue = {note.note} onChangeText={setCurrentNote}/>
            {global_access()}

            <View style={styles.row}>
            {(currentNote != undefined && currentNote != note.note && currentNote != '')?
            <TouchableOpacity style={{fontSize: 20,borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
            onPress={updateNote}>
              <Image source={require('../assets/header.png')} style={styles.square_button}/>
            </TouchableOpacity>:null}

            {(currentContent != undefined && currentContent != note.content)? 
            <TouchableOpacity style={{fontSize: 20,borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
            onPress={()=>{updateContent('content', currentContent)}}>
              <Image source={require('../assets/save.png')} style={styles.square_button}/>
            </TouchableOpacity>:null}
            </View>
          </View>

          <ScrollView style={{marginLeft:10,marginRight:10}}>
            <View>
              {/* <Text style={styles.textup}>{note.user3_id}</Text> */}
              <TextInput style={styles.textdown} editable multiline placeholder={'Content...'} defaultValue = {note.content_user3} onChangeText={setCurrentContent} />
              <Text style={styles.textup}>{note.user_id}</Text>
              <Text style={styles.textdown}>{note.content}</Text>
              <Text style={styles.textup}>{note.user1_id}</Text>
              <Text style={styles.textdown}>{note.content_user1}</Text>
              <Text style={styles.textup}>{note.user2_id}</Text>
              <Text style={styles.textdown}>{note.content_user2}</Text>
            </View>
          </ScrollView>

        </View>
      );
    });
  };

  const comparelogin = () => {
    (<View><Text>{user_id} {JSON.stringify(notes)}</Text></View>)
    if (user_id == notes[0].user_id || '-1' == notes[0].user_id){return (showAsUser_id())}
    else if (user_id == notes[0].user1_id){return (showAsUser1_id())}

    else if (user_id == notes[0].user2_id){return (showAsUser2_id())}

    else if (user_id == notes[0].user3_id){return (showAsUser3_id())}
    else{return <View style={styles.loading}><Text>You can`t read and write this note</Text></View>}
    
  }

  
// MAIN RETURN

  if (isLoading) {
    if (user_id != undefined && notes[0] != undefined){setIsLoading(false),comparelogin()}
    else{update(),select_id(),console.log('loading')}
    return (
      <SafeAreaView style={styles.loading}>
        <StatusBar animated = {true} hidden = {true} />
        <Text>Loading...</Text>
      </SafeAreaView>
    );
  }else{return (
    <SafeAreaView  style={styles.container}>
      <StatusBar animated = {true} hidden = {true} />
      {comparelogin()}
      {/* INCLUDE UPDATE()  */}
      
    </SafeAreaView>
  ); }
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
    alignItems: 'center',
    alignSelf: 'stretch',
    justifyContent: 'space-between',
    margin: 4,
    padding: 8,
  },

  
  textup: {
    fontSize: 30,
  },

  textdown: {
    fontSize: 20,
  },

  square_button: {
    height:30,
    width:30,
    margin: 8
  }

});
