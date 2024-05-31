#include<stdio.h>
#include<math.h>

void print_int(int n){
    printf("%d\n",n);
}

void print_string(char s[]){
    printf("%s\n",s);
}

void print_float(float f){
    printf("%f\n",f);
}

void print_char(char c){
    printf("%c\n",c);
}

void print_array_int(int* j){
    printf("[");
    size_t size = sizeof(j) / sizeof(j[0]);
    for (size_t i = 0; i < size; i++)
    {
        printf("%d, ", j[i]);
    }
    printf("]\n"); 
}

int power_int(int target, int n){
    int result = 1;
    while (n > 0){
        result = result * target;
        n = n -1;
    }
    return result;
}

float power_float(float target, float n){

    return pow(target, n);
}

void print_matrix_int(int rows, int cols, int **j){
    
    for (size_t i = 0; i < rows; i++)
    {
        printf("[");
        for (size_t k = 0; k < cols; k++)
        {
           printf("%d", j[i][k]); 
           if (k < cols - 1) {
                printf(", ");
            }
        } 
        printf("]\n"); 
    }
}

void print_array_float(float *j){
    printf("[");
    for (size_t i = 0; i < (sizeof( j ) / sizeof( j[0])); i++)
    {
        printf("%f, ", j[i]);
    }
    printf("]\n"); 
}