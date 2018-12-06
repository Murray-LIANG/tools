
ospt_cmd='ospt --storops_unity 10.245.83.243 --username admin --password Password123!'

log_dir="${1:-$(date +'%Y%m%d_%H%M%S')}"
mkdir -p "${log_dir}"

concurrencies="10 20 30 40"
repeat=3


function fatal() {
    cat <<< "FATAL! $@" 1>&2
    exit 1
}


function pt_create_delete() {
    for num in ${concurrencies}; do
        for i in $(seq ${repeat}); do
            ${ospt_cmd} --log ${log_dir}/create-volumes-${num}-${i}.log \
                create-volumes --tag liangr --count ${num} \
                && ${ospt_cmd} --log ${log_dir}/delete-volumes-${num}-${i}.log \
                delete-volumes --tag liangr --count ${num} \
                || fatal "Error in performance test of creating/deleting volumes"
        done
    done
}


function prepare_luns_hosts() {
    max_num_luns=${concurrencies##* }
    ${ospt_cmd} --log ${log_dir}/prepare-volumes.log create-volumes --tag liangr --count ${max_num_luns} \
        && ${ospt_cmd} --log ${log_dir}/prepare-servers.log create-servers --tag liangr --count ${max_num_luns} \
        || fatal "Error in preparing luns and hosts"
}


function pt_attach_detach() {
    for num in ${concurrencies}; do
        for i in $(seq ${repeat}); do
            ${ospt_cmd} --log ${log_dir}/attach-${num}-${i}.log attach --tag liangr --count ${num} \
                && ${ospt_cmd} --log ${log_dir}/detach-${num}-${i}.log detach --tag liangr --count ${num} \
                || fatal "Error in performance test of attaching/detaching"
        done
    done
}


function cleanup_luns_hosts() {
    ${ospt_cmd} --log ${log_dir}/cleanup-volumes.log delete-volumes --tag liangr --count ${max_num_luns} \
        && ${ospt_cmd} --log ${log_dir}/delete-servers.log delete-servers --tag liangr --count ${max_num_luns} \
        || fatal "Error in cleaning up"
}


function collect_time() {
    #pattern='s/.*Thread-\([0-9]*\) .*TIME: \([0-9\.]*\),.*/\1\t\2/p'
    pattern='s/.*TIME: \([0-9\.]*\),.*/\1/p'
    add=''
    title=''
    for i in $(seq ${repeat}); do
        add+="\$${i}+"
        title+="Round #${i}\t"
    done
    add=${add%+}
    title+='Avg.'
    
    for num in ${concurrencies}; do
        for act in create-volumes delete-volumes attach detach; do
            for i in $(seq ${repeat}); do
                sed -n "${pattern}" ${log_dir}/${act}-${num}-${i}.log > ${log_dir}/${act}-${num}-${i}.time
            done
            paste ${log_dir}/${act}-${num}-*.time > ${log_dir}/${act}-${num}.time
            awk -v OFS='\t' '{ print $0,('${add}')/'${repeat}' }' ${log_dir}/${act}-${num}.time > ${log_dir}/${act}-${num}.csv
            sed -i '1 i\'"${title}" ${log_dir}/${act}-${num}.csv
        done
    done
}

