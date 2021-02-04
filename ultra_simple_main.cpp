/*
 *  RPLIDAR
 *  Ultra Simple Data Grabber Demo App
 *
 *  Copyright (c) 2009 - 2014 RoboPeak Team
 *  http://www.robopeak.com
 *  Copyright (c) 2014 - 2019 Shanghai Slamtec Co., Ltd.
 *  http://www.slamtec.com
 *
 */

/*
 * HISTORICAL INFORMATION -
 *
 *  2021-01-25  msipin  Added this header. Moved creation of array out of loop for increased performance
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "rplidar.h" //RPLIDAR standard sdk, all-in-one header

#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

#ifdef _WIN32
#include <Windows.h>
#define delay(x)   ::Sleep(x)
#else
#include <unistd.h>
static inline void delay(_word_size_t ms){
    while (ms>=1000){
        usleep(1000*1000);
        ms-=1000;
    };
    if (ms!=0)
        usleep(ms*1000);
}
#endif

using namespace rp::standalone::rplidar;

bool checkRPLIDARHealth(RPlidarDriver * drv)
{
    u_result     op_result;
    rplidar_response_device_health_t healthinfo;


    op_result = drv->getHealth(healthinfo);
    if (IS_OK(op_result)) { // the macro IS_OK is the preperred way to judge whether the operation is succeed.
        printf("RPLidar health status : %d\n", healthinfo.status);
        if (healthinfo.status == RPLIDAR_STATUS_ERROR) {
            fprintf(stderr, "Error, rplidar internal error detected. Please reboot the device to retry.\n");
            // enable the following code if you want rplidar to be reboot by software
            // drv->reset();
            return false;
        } else {
            return true;
        }

    } else {
        fprintf(stderr, "Error, cannot retrieve the lidar health code: %x\n", op_result);
        return false;
    }
}

#include <signal.h>
bool ctrl_c_pressed=false;
void ctrlc(int)
{
    // Reassert signal control, in case a new signal arrives before we're done
    signal(SIGINT, ctrlc);
    ctrl_c_pressed = true;
}

int main(int argc, const char * argv[]) {
    const char * opt_com_path = NULL;
    _u32         baudrateArray[2] = {115200, 256000};
    _u32         opt_com_baudrate = 0;
    u_result     op_result;
    //rplidar_response_measurement_node_hq_t nodes[8192];
    rplidar_response_measurement_node_t nodes[10240];
    size_t   count = _countof(nodes);
    char filename[99+1];
    //sprintf(filename,"/dev/shm/000"); // FOR TESTING, ONLY!!
    struct data {
        float range;
        int cnt;
    };
    data arr[360+1];

    bool useArgcBaudrate = false;

    printf("Ultra simple LIDAR data grabber for RPLIDAR.\n"
           "Version: " RPLIDAR_SDK_VERSION "\n");

    // read serial port from the command line...
    if (argc>1) opt_com_path = argv[1]; // or set to a fixed value: e.g. "com3" 

    // read baud rate from the command line if specified...
    if (argc>2)
    {
        opt_com_baudrate = strtoul(argv[2], NULL, 10);
        useArgcBaudrate = true;
    }

    if (!opt_com_path) {
#ifdef _WIN32
        // use default com port
        opt_com_path = "\\\\.\\com57";
#elif __APPLE__
        opt_com_path = "/dev/tty.SLAB_USBtoUART";
#else
        opt_com_path = "/dev/ttyUSB0";
#endif
    }

    // create the driver instance
	RPlidarDriver * drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
    if (!drv) {
        fprintf(stderr, "insufficent memory, exit\n");
        exit(-2);
    }
    
    rplidar_response_device_info_t devinfo;
    bool connectSuccess = false;
    // make connection...
    if(useArgcBaudrate)
    {
        if(!drv)
            drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
        if (IS_OK(drv->connect(opt_com_path, opt_com_baudrate)))
        {
            op_result = drv->getDeviceInfo(devinfo);

            if (IS_OK(op_result)) 
            {
                connectSuccess = true;
            }
            else
            {
                delete drv;
                drv = NULL;
            }
        }
    }
    else
    {
        size_t baudRateArraySize = (sizeof(baudrateArray))/ (sizeof(baudrateArray[0]));
        for(size_t i = 0; i < baudRateArraySize; ++i)
        {
            if(!drv)
                drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
            if(IS_OK(drv->connect(opt_com_path, baudrateArray[i])))
            {
                op_result = drv->getDeviceInfo(devinfo);

                if (IS_OK(op_result)) 
                {
                    connectSuccess = true;
                    break;
                }
                else
                {
                    delete drv;
                    drv = NULL;
                }
            }
        }
    }
    if (!connectSuccess) {
        
        fprintf(stderr, "Error, cannot bind to the specified serial port %s.\n"
            , opt_com_path);
        goto on_finished;
    }

    // print out the device serial number, firmware and hardware version number..
    printf("RPLIDAR S/N: ");
    for (int pos = 0; pos < 16 ;++pos) {
        printf("%02X", devinfo.serialnum[pos]);
    }

    printf("\n"
            "Firmware Ver: %d.%02d\n"
            "Hardware Rev: %d\n"
            , devinfo.firmware_version>>8
            , devinfo.firmware_version & 0xFF
            , (int)devinfo.hardware_version);



    // check health...
    if (!checkRPLIDARHealth(drv)) {
        goto on_finished;
    }

    signal(SIGINT, ctrlc);
    
    drv->startMotor();
    // start scan...
    drv->startScan(0,1);
    //drv->startScan(0,0);


    // fetech result and print it out...
    while (!ctrl_c_pressed) {


        op_result = drv->grabScanData(nodes, count);
        // HQ - if (IS_OK(op_result)) {
        // "REGULAR" -
        if (IS_OK(op_result) || op_result == RESULT_OPERATION_TIMEOUT) {
            drv->ascendScanData(nodes, count);
            printf("\n\tCOUNT: %d\n\n",(int)count);

            //  HQ RESULTS -
            //  printf("%s angle: %3.2f Dist(mm): %8.2f Quality: %d \n", 
            //      (nodes[pos].flag & RPLIDAR_RESP_MEASUREMENT_SYNCBIT) ?"S ":"  ", 
            //      (nodes[pos].angle_z_q14 * 90.f / (1 << 14)), 
            //      nodes[pos].dist_mm_q2/4.0f,
            //      nodes[pos].quality);

            //  "REGULAR" RESULTS -
            //  printf("%s theta: %03.2f Dist: %08.2f \n",
            //      (nodes[pos].sync_quality & RPLIDAR_RESP_MEASUREMENT_SYNCBIT) ?"S ":"  ",
            //      (nodes[pos].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT)/64.0f,
            //      nodes[pos].distance_q2/4.0f);


            // Walk through the samples
            memset((void *)arr,0,sizeof(arr));
            for (int idx=0;idx < (int)count;idx++) {

                // Calculate range
                // Calculate theta
                // HQ - theta = (nodes[pos].angle_z_q14 * 90.f / (1 << 14)); 
                // "REGULAR" -
//  struct data {
//      float range;
//      int cnt;
//  };
//  data arr[360+1];
                int hdg = (int)((nodes[idx].angle_q6_checkbit >> RPLIDAR_RESP_MEASUREMENT_ANGLE_SHIFT)/64.0f);
                float rng = nodes[idx].distance_q2/4.0f;
                if ((hdg >= 0) && (hdg < 360) && (rng > 0.0)) {
                    arr[hdg].range += rng;
                    arr[hdg].cnt++;
                    //printf("THT: %3d  DST: %8.2f  QUALITY: ?\n", hdg, rng);
                }

            } // Done, walking through all returned data

            for (int hdg=0;hdg < 360;hdg++) {
                float range = -1.0f;
                // Calculate average distance
                if (arr[hdg].cnt > 0) {
                    range = (arr[hdg].range/arr[hdg].cnt);

                }
                // Print heading, range, quality
                printf("HDG: %3d  RNG: %8.2f  QUALITY: ?\n", hdg, range);

                // Save range in filesystem
                sprintf(filename,"/dev/shm/%03d",hdg);
                filename[99] = '\0';
                FILE *fp = fopen(filename,"w");
                if (fp != NULL) {
                    fprintf(fp,"%0.2f",range);
                    // Close file
                    fclose(fp);
                }
            }

        } // op_rslt is OK

    }

    drv->stop();
    drv->stopMotor();
    // done!
on_finished:
    RPlidarDriver::DisposeDriver(drv);
    drv = NULL;
    return 0;
}

