import { Text, StyleSheet, View, TextInput, Alert, Button } from 'react-native';
import React, { useState } from 'react';

export default function Formulario() {

  const [Nombre, setNombre] = useState('');

  // Esta se ejecutará directamente en el celular
  const mostrarAlerta = () => {
    if (Nombre.trim() === '') {
      alert('Error, por favor ingresa tu nombre');
      Alert.alert('Error', 'Por favor ingresa tu nombre');
    } else {
      Alert.alert(`${Nombre}!, Tu nombre ha sido registrado`);
      setNombre('');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Ingresa tu nombre:</Text>

      <TextInput
        style={styles.input}
        placeholder='Ej. Isabella'
        value={Nombre}
        onChangeText={setNombre}
        keyboardType='default'
        autoCapitalize='words'
      />

       <TextInput
        style={styles.input}
        placeholder='Contraseña'
        keyboardType='numeric'
        secureTextEntry={true}
      />

      <TextInput
        style={styles.input}
        multiline={true}
        numberOfLines={4}
      />

      
        <Button
          title="Saludar"
          onPress={mostrarAlerta}
          color="purple"
        />
      </View>
  
  );
}

// Estilos
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  label: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  input: {
    height: 50,
    borderColor: 'gray',
    borderWidth: 1, // Borde del input
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 20,
    fontSize: 16,
    backgroundColor: 'white',
  },
  buttonContainer: {
    borderRadius: 10,
    overflow: 'hidden', // Para que el botón respete los bordes redondeados
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 5, 
  },
});