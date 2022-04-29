using System;
using System.ComponentModel;
using System.Linq;
using thumbnailService.Context;
using thumbnailService.Entities.Sql;
using thumbnailService.Models;

namespace thumbnailService.Converters;

public static class JobConverter
{
    public static JobFullInformation ToJobFullInformation(this Entities.Sql.Jobs input, ModelThumbnailDBContext context)
    {
        Jobstatus status = context.Jobstatus.FirstOrDefault(s => s.Id.Equals(input.Id));
        var converter = TypeDescriptor.GetConverter(typeof(JobStatus));
        var statusString = converter.ConvertToString(status);
        
        Enum.TryParse(statusString, out JobStatus jobStatus);

        return new JobFullInformation(input.Name, input.Id, jobStatus);
    }
}
