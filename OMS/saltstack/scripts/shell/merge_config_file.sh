#!/bin/sh


sourceBasePath=$1   # 源基本路径:  /srv/salt/app_config
targetBasePath=$2   # 目标基本路径: /srv/salt/merge_config
zoneList=$3         # 分区列表: (s2043 s2044 s2045 s2046)
mergePathName=$4    # 合并目录名: s2043_s2044_s2045_s2046
projectName=$5      # 项目名



comparing(){
    file1=$1
    file2=$2
    file3=$1

    diff -DVERSION1 ${file1} ${file2} | grep -v '^#ifdef' | grep -v '^#else' | grep -v "^#endif" | grep -v "ifndef" > ${file3}.tmp

    if [ $? -eq 0 ];then
        echo "merge file success"
        cp -rf ${file3}.tmp ${file1} && rm -rf ${file3}.tmp
    else
        echo "merge file failed!"
        exit 1
    fi
}



if [ ! "$#" -eq 5 ];then
    echo "Usage: $0 source_path, merge_path, zone_shell_array, merge_name, project_name"
    exit 1
fi

for zone in ${zoneList[@]};do
    if [ ${projectName} == 'war_data' ];then
        source_abs_path=${sourceBasePath}/${zone}/${projectName}/${projectName}/WEB-INF
        target_abs_path=${targetBasePath}/${mergePathName}/${projectName}/${projectName}/WEB-INF
    else
        :
    fi

    if [ -d ${source_abs_path} ];then
        cd ${source_abs_path}
        fileList=$(ls -l | awk '{print $9}' | grep -v ^$)               # 获得文件列表
    fi

    for filename in ${fileList[@]}; do
        configFile=${source_abs_path}/${filename}                       # 源文件
        if [ ! -f ${configFile} ];then
            echo "${configFile} not found"
            exit 1
        fi

        if [ ! -d ${target_abs_path} ];then
            mkdir -p ${target_abs_path}
        fi

        targetFile=${target_abs_path}/${filename}                       # 目标文件
        if [ ! -f ${targetFile} ];then
            touch ${targetFile}
        fi
        comparing ${targetFile} ${configFile}
    done
done

exit 0