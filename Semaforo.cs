using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Semaforo : MonoBehaviour
{
    public GameObject luz;

    public Transform posVerde;
    public Transform posAmarilla;
    public Transform posRoja;

    private enum EstadoSemaforo { Verde, Amarillo, Rojo }
    private EstadoSemaforo estadoActual;

    private void Start()
    {
        estadoActual = EstadoSemaforo.Verde;
        StartCoroutine(CicloSemaforo());
    }

    void Update()
    {
        switch (estadoActual)
        {
            case EstadoSemaforo.Verde:
                luz.transform.position = posVerde.position;
                luz.GetComponent<Light>().color = new Color32(61, 161, 27, 255);
                break;
            case EstadoSemaforo.Amarillo:
                luz.transform.position = posAmarilla.position;
                luz.GetComponent<Light>().color = Color.yellow;
                break;
            case EstadoSemaforo.Rojo:
                luz.transform.position = posRoja.position;
                luz.GetComponent<Light>().color = Color.red;
                break;
        }
    }

    IEnumerator CicloSemaforo()
    {
        while (true)
        {
            if (estadoActual == EstadoSemaforo.Verde)
            {
                yield return new WaitForSeconds(5); // Tiempo en verde
                estadoActual = EstadoSemaforo.Amarillo;
            }
            else if (estadoActual == EstadoSemaforo.Amarillo)
            {
                yield return new WaitForSeconds(3); // Tiempo en amarillo
                estadoActual = EstadoSemaforo.Rojo;
            }
            else if (estadoActual == EstadoSemaforo.Rojo)
            {
                yield return new WaitForSeconds(5); // Tiempo en rojo
                estadoActual = EstadoSemaforo.Verde;
            }
        }
    }
}
